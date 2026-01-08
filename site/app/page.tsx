'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Cpu, Network, BookOpen, ShieldAlert, Code, Lock, Download, Activity, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// --- CONFIGURATION ---
const SITE_CONFIG = {
    name: "Dino Ilievski",
    handle: "ilievski.sh", // UPDATED: High Signal Domain
    status: "BUILDING PHASE I (OUROBOROS)",
    location: "SAN FRANCISCO",
    email: "dino.ilievski@gmail.com",
    dopamineLabUrl: "https://dino-dopamine.streamlit.app" // UPDATE THIS AFTER DEPLOYING STREAMLIT
};

// --- DATA: SYSTEM AUDIT LOG ---
const AUDIT_LOG = [
    {
        timestamp: "2018-Q3",
        operation: "DEEP_DUE_DILIGENCE",
        target: "M&A_PORTFOLIO_SIMULATION",
        value: "$18B",
        outcome: "RISK_MITIGATED",
        notes: "Audited high-variance legal constraints in multi-billion dollar mergers."
    },
    {
        timestamp: "2020-Q1",
        operation: "MECHANISM_DESIGN",
        target: "ALGORITHMIC_POLICY_V1",
        compiler: "U.S._CONGRESS",
        outcome: "DEPLOYED",
        notes: "Drafted computational policy frameworks for federal oversight."
    },
    {
        timestamp: "CURRENT",
        operation: "KERNEL_ORCHESTRATION",
        target: "MULTI_AGENT_SYSTEMS",
        stack: ["Python", "LangChain", "RAG"],
        status: "ACTIVE",
        notes: "Translating civilizational rules (Law) into executable agentic logic."
    }
];

const MANIFESTO = [
    { year: "Y01-07", phase: "PHASE I: OUROBOROS", desc: "Agentic Modeling for Macro-Strategy. Building the initial prediction engines." },
    { year: "Y08-15", phase: "PHASE II: NEXUS", desc: "The Corporate Digital Twin. Integration into high-value economic nodes." },
    { year: "Y31-45", phase: "PHASE IV: THE KERNEL", desc: "Global Clearinghouse for Intent. The map becomes the territory." },
];

// --- COMPONENTS ---

const Typewriter = ({ text, delay = 0 }: { text: string; delay?: number }) => {
    const [displayedText, setDisplayedText] = useState('');
    useEffect(() => {
        const timeout = setTimeout(() => {
            let i = 0;
            const timer = setInterval(() => {
                setDisplayedText(text.substring(0, i + 1));
                i++;
                if (i === text.length) clearInterval(timer);
            }, 30);
            return () => clearInterval(timer);
        }, delay);
        return () => clearTimeout(timeout);
    }, [text, delay]);
    return <span>{displayedText}</span>;
};

export default function TerminalLanding() {
    const [wireheadMode, setWireheadMode] = useState(false);
    const [command, setCommand] = useState('');
    const [sudoAccess, setSudoAccess] = useState(false);
    const [passwordPrompt, setPasswordPrompt] = useState(false);

    // Easter Egg Logic
    const handleCommand = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            if (passwordPrompt) {
                if (command.toLowerCase() === 'ouroboros') {
                    setSudoAccess(true);
                    setPasswordPrompt(false);
                    setCommand('');
                    setWireheadMode(true); // Auto-trigger wirehead on root access
                } else {
                    setCommand('ACCESS_DENIED');
                    setTimeout(() => setCommand(''), 1000);
                }
            } else {
                if (command.toLowerCase() === 'sudo') {
                    setPasswordPrompt(true);
                    setCommand('');
                } else if (command.toLowerCase() === 'whoami') {
                    setCommand('ARCHITECT');
                } else {
                    setCommand('COMMAND_NOT_FOUND');
                    setTimeout(() => setCommand(''), 1000);
                }
            }
        }
    };

    return (
        <div className={`min-h-screen font-mono p-4 md:p-12 selection:bg-green-900 selection:text-green-100 transition-colors duration-500 
      ${wireheadMode ? 'bg-zinc-950 text-amber-500' : 'bg-black text-green-500'}`}>

            {/* --- HEADER --- */}
            <header className="flex flex-col md:flex-row justify-between text-xs border-b border-green-900/50 pb-4 mb-12 opacity-80">
                <div className="flex flex-col md:flex-row gap-4">
                    <span>USER: {sudoAccess ? 'ROOT (ARCHITECT)' : 'GUEST'}</span>
                    <span>LOCATION: {SITE_CONFIG.location}</span>
                    <span>STATUS: <span className="animate-pulse">{SITE_CONFIG.status}</span></span>
                </div>
                <div className="mt-2 md:mt-0 text-right">
                    SYS_TIME: {new Date().toISOString().split('T')[0]}
                </div>
            </header>

            {/* --- HERO --- */}
            <main className="max-w-5xl mx-auto space-y-24">

                <section className="space-y-6">
                    <div className="text-4xl md:text-6xl font-bold tracking-tighter">
                        <span className="mr-2">{'>'}</span>
                        <Typewriter text="INITIALIZING COMPUTATIONAL GOVERNANCE..." delay={100} />
                        <span className="animate-blink">_</span>
                    </div>
                    <p className="text-xl opacity-90 leading-relaxed max-w-2xl">
                        <Typewriter text="Architecting the Civilizational Kernel. Translating legal constraints into agentic logic." delay={2000} />
                    </p>

                    <div className="flex gap-4 pt-4">
                        <a href={SITE_CONFIG.dopamineLabUrl} target="_blank" rel="noreferrer"
                            className={`px-4 py-2 border hover:bg-green-500 hover:text-black transition-all flex items-center gap-2
              ${wireheadMode ? 'border-amber-500 hover:bg-amber-500' : 'border-green-500'}`}>
                            <Activity size={16} /> ENTER_THE_LAB
                        </a>
                        <button
                            onClick={() => document.getElementById('audit-log')?.scrollIntoView({ behavior: 'smooth' })}
                            className="px-4 py-2 border border-dashed border-opacity-50 hover:border-opacity-100 transition-all opacity-70 hover:opacity-100">
                            VIEW_SYSTEM_AUDIT
                        </button>
                    </div>
                </section>

                {/* --- AUDIT LOG (REPLACES RESUME) --- */}
                <section id="audit-log" className="space-y-6">
                    <div className="flex items-center gap-2 text-lg font-bold border-b border-green-900/50 pb-2">
                        <ShieldAlert size={20} />
                        <h2>SYSTEM_AUDIT_LOG</h2>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="w-full text-xs md:text-sm text-left opacity-90">
                            <thead className="opacity-50 border-b border-green-900/30">
                                <tr>
                                    <th className="py-2">TIMESTAMP</th>
                                    <th className="py-2">OPERATION</th>
                                    <th className="py-2">TARGET</th>
                                    <th className="py-2">OUTCOME</th>
                                </tr>
                            </thead>
                            <tbody>
                                {AUDIT_LOG.map((log, idx) => (
                                    <tr key={idx} className="border-b border-green-900/10 hover:bg-green-900/5 transition-colors group">
                                        <td className="py-3 font-bold opacity-60">{log.timestamp}</td>
                                        <td className="py-3 font-bold text-green-300">{log.operation}</td>
                                        <td className="py-3">{log.target}</td>
                                        <td className="py-3">
                                            <span className={`px-1 ${log.outcome === 'RISK_MITIGATED' || log.outcome === 'DEPLOYED' ? 'bg-green-900/30 text-green-300' : 'bg-blue-900/30 text-blue-300'}`}>
                                                {log.outcome}
                                            </span>
                                        </td>
                                        <td className="py-3 opacity-0 group-hover:opacity-60 hidden md:table-cell italic max-w-xs truncate">
                      // {log.notes}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* --- THE LAB: PROOF OF COMPETENCE --- */}
                <section className="space-y-8">
                    <div className="flex items-center gap-2 text-lg font-bold border-b border-green-900/50 pb-2">
                        <Terminal size={20} />
                        <h2>ACTIVE_EXPERIMENTS</h2>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Project A: Dopamine Agent */}
                        <div className={`border p-6 hover:bg-green-900/10 transition-colors relative group
              ${wireheadMode ? 'border-amber-900/50' : 'border-green-900/50'}`}>
                            <div className="absolute top-2 right-2 opacity-30 group-hover:opacity-100 transition-opacity">
                                <Network size={40} />
                            </div>
                            <h3 className="text-xl font-bold mb-2">THE DOPAMINE AGENT</h3>
                            <p className="text-sm opacity-80 mb-4 h-16">
                                Reinforcement Learning agent with biological reward prediction error parameters.
                                Simulates addiction loops in deterministic environments.
                            </p>
                            <div className="flex gap-4 text-xs font-mono opacity-60">
                                <span>SHA-256: 7d4f...9a2b</span>
                                <span>STATUS: LIVE</span>
                            </div>
                        </div>

                        {/* Project B: Sigil AI */}
                        <div className={`border p-6 hover:bg-green-900/10 transition-colors relative group
              ${wireheadMode ? 'border-amber-900/50' : 'border-green-900/50'}`}>
                            {/* PLACEHOLDER FOR DIAGRAM IMAGE */}
                            <div className="h-32 w-full bg-green-900/20 mb-4 flex items-center justify-center border border-dashed border-green-900/40">
                                <img src="/sigil-diagram.png" alt="Sigil Architecture" className="h-full w-full object-cover opacity-80 hover:opacity-100" />
                            </div>
                            <h3 className="text-xl font-bold mb-2">SIGIL_AI // MICRO-KERNEL</h3>
                            <p className="text-sm opacity-80 mb-4">
                                Multi-agent simulation where "Patient" and "Clinician" agents stress-test clinical workflows.
                            </p>
                            <div className="flex gap-4 text-xs font-mono opacity-60">
                                <a href="#" className="hover:text-white hover:underline decoration-1 underline-offset-4 flex items-center gap-1">
                                    <Code size={12} /> VIEW_SOURCE
                                </a>
                            </div>
                        </div>
                    </div>
                </section>

                {/* --- MANIFESTO DOWNLOAD --- */}
                <section className="border border-green-900/50 p-6 flex flex-col md:flex-row justify-between items-center gap-4 bg-green-900/5">
                    <div>
                        <h3 className="text-lg font-bold flex items-center gap-2">
                            <BookOpen size={18} /> CIVILIZATIONAL_KERNEL_MANIFESTO.PDF
                        </h3>
                        <p className="text-xs opacity-60 mt-1 font-mono">CHECKSUM: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</p>
                    </div>
                    <button className="px-6 py-3 bg-green-900/20 hover:bg-green-500 hover:text-black border border-green-500 transition-all flex items-center gap-2 font-bold text-sm">
                        <Download size={16} /> DOWNLOAD_DOCUMENT
                    </button>
                </section>

            </main>

            {/* --- FOOTER / SHELL INPUT --- */}
            <footer className="fixed bottom-0 left-0 w-full p-2 bg-black border-t border-green-900/50 flex justify-between items-center text-xs z-50 font-mono">
                <div className="flex items-center gap-2 w-full max-w-lg">
                    <span className="text-green-500 opacity-50 whitespace-nowrap hidden md:block">
                        {sudoAccess ? 'root@ilievski.sh:~#' : 'guest@ilievski.sh:~$'}
                    </span>
                    <span className="text-green-500 opacity-50 whitespace-nowrap md:hidden">
                        {'>'}
                    </span>

                    <input
                        type={passwordPrompt ? "password" : "text"}
                        value={command}
                        onChange={(e) => setCommand(e.target.value)}
                        onKeyDown={handleCommand}
                        className="bg-transparent border-none outline-none text-green-500 w-full placeholder-green-900/50"
                        placeholder={passwordPrompt ? "ENTER_PASSWORD..." : "TYPE 'sudo' FOR ROOT ACCESS..."}
                        autoComplete="off"
                    />
                </div>
                <div className="flex gap-4 opacity-50 hidden md:flex">
                    <span>GITHUB</span>
                    <span>LINKEDIN</span>
                </div>
            </footer>
        </div>
    );
}
