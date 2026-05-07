"""
Crew Orchestrator utama — mengelola semua agent OSINT
"""

import os
from crewai import Crew, Process
from crewai.project import CrewBase, agent, crew, task

from src.agents.social_scout import create_social_scout
from src.agents.domain_intel import create_domain_intel
from src.agents.email_hunter import create_email_hunter
from src.agents.ip_recon import create_ip_recon
from src.agents.report_writer import create_report_writer

from src.tasks.osint_tasks import OsintTasks
from src.utils.target_detector import detect_target_type
from src.utils.report_saver import save_report


class OsintCrew:
    """
    Orchestrator utama untuk semua agent OSINT.
    Menentukan agent mana yang dijalankan berdasarkan tipe target.
    """

    def __init__(
        self,
        target: str,
        target_type: str = "auto",
        output_format: str = "markdown",
        verbose: bool = False,
    ):
        self.target = target
        self.output_format = output_format
        self.verbose = verbose

        # Auto-detect tipe target
        if target_type == "auto":
            self.target_type = detect_target_type(target)
            print(f"Auto-detected tipe target: {self.target_type}")
        else:
            self.target_type = target_type

        # Inisialisasi agents
        self.agents = self._init_agents()
        self.tasks_builder = OsintTasks(target=self.target, target_type=self.target_type)

    def _init_agents(self):
        """Inisialisasi hanya agent yang relevan dengan target"""
        agents = {}

        # Report writer selalu ada
        agents["report_writer"] = create_report_writer()

        # Agent berdasarkan tipe target
        if self.target_type in ["username", "fullname"]:
            agents["social_scout"] = create_social_scout()

        if self.target_type in ["domain", "ip"]:
            agents["domain_intel"] = create_domain_intel()
            agents["ip_recon"] = create_ip_recon()

        if self.target_type in ["email"]:
            agents["email_hunter"] = create_email_hunter()
            agents["social_scout"] = create_social_scout()

        # Jika auto/unknown — jalankan semua agent
        if self.target_type == "unknown":
            agents["social_scout"] = create_social_scout()
            agents["domain_intel"] = create_domain_intel()
            agents["email_hunter"] = create_email_hunter()
            agents["ip_recon"] = create_ip_recon()

        print(f"Agent aktif: {', '.join(agents.keys())}")
        return agents

    def _build_tasks(self):
        """Build task list berdasarkan agent yang aktif"""
        tasks = []

        if "social_scout" in self.agents:
            tasks.append(
                self.tasks_builder.social_media_task(self.agents["social_scout"])
            )

        if "domain_intel" in self.agents:
            tasks.append(
                self.tasks_builder.domain_recon_task(self.agents["domain_intel"])
            )

        if "email_hunter" in self.agents:
            tasks.append(
                self.tasks_builder.email_hunt_task(self.agents["email_hunter"])
            )

        if "ip_recon" in self.agents:
            tasks.append(
                self.tasks_builder.ip_recon_task(self.agents["ip_recon"])
            )

        # Report task selalu di akhir, dengan context dari semua task sebelumnya
        report_task = self.tasks_builder.compile_report_task(
            self.agents["report_writer"],
            context_tasks=tasks,
            output_format=self.output_format,
        )
        tasks.append(report_task)

        return tasks

    def run(self):
        """Jalankan crew OSINT"""
        tasks = self._build_tasks()
        active_agents = list(self.agents.values())

        osint_crew = Crew(
            agents=active_agents,
            tasks=tasks,
            process=Process.sequential,  # Sequential: satu per satu
            verbose=self.verbose,
        )

        print(f"\nMemulai investigasi OSINT untuk: {self.target}")
        print(f"Jumlah agent aktif: {len(active_agents)}")
        print(f"Jumlah task: {len(tasks)}")
        print("-" * 40)

        result = osint_crew.kickoff()

        # Simpan hasil
        saved_path = save_report(
            content=str(result),
            target=self.target,
            output_format=self.output_format,
        )
        print(f"\nLaporan disimpan: {saved_path}")

        return result
