"use client";

import React, { useState, useRef, useEffect } from "react";
import { startInterview, submitAnswer, exportReport } from "@/lib/api";
import { Send, User, Bot, Loader2, Download, Mic, MicOff } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { AuroraBackground } from "./ui/AuroraBackground";
import { GlassCard } from "./ui/GlassCard";
import { MagneticButton } from "./ui/MagneticButton";

interface Message {
    id: string;
    sender: "user" | "bot";
    text: string;
    round?: string;
    feedback?: { score: number; feedback: string };
}

export default function InterviewChat() {
    const [candidateName, setCandidateName] = useState("");
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [completed, setCompleted] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Speech to Text State
    const [isListening, setIsListening] = useState(false);
    const recognitionRef = useRef<any>(null);

    useEffect(() => {
        if (typeof window !== 'undefined' && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
            recognitionRef.current = new SpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = true;

            recognitionRef.current.onresult = (event: any) => {
                const transcript = Array.from(event.results)
                    .map((result: any) => result[0])
                    .map((result) => result.transcript)
                    .join('');
                setInput(transcript);
            };

            recognitionRef.current.onend = () => setIsListening(false);
            recognitionRef.current.onerror = (event: any) => {
                console.error("Speech recognition error", event.error);
                setIsListening(false);
            };
        }
    }, []);

    const toggleListening = () => {
        if (isListening) {
            recognitionRef.current?.stop();
        } else {
            setInput(""); // Clear input when starting new speech
            recognitionRef.current?.start();
            setIsListening(true);
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const [debugLogs, setDebugLogs] = useState<string[]>([]);

    const log = (msg: string) => {
        console.log(msg);
        setDebugLogs(prev => [...prev, `${new Date().toISOString().split('T')[1].split('.')[0]} ${msg}`]);
    };

    const handleStart = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!candidateName.trim()) return;

        setLoading(true);
        log("Starting interview...");
        try {
            const data = await startInterview(candidateName);
            log(`Response Rcvd: ${JSON.stringify(data).substring(0, 50)}...`);

            if (data && data.session_id && data.initial_action) {
                setSessionId(data.session_id);
                addMessage("bot", data.initial_action.question.text, data.initial_action.question.round);
                log("State Updated with Message");
            } else {
                log("Invalid Data Structure");
                alert("Failed to initialize session. Invalid server response.");
            }
        } catch (error: any) {
            log(`Error: ${error.message || error}`);
            console.error("Failed to start:", error);
            alert("Error starting interview. See debug log.");
        } finally {
            setLoading(false);
        }
    };

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !sessionId || loading) return;

        const userText = input;
        setInput("");
        setIsListening(false); // Ensure listening stops on send
        addMessage("user", userText);
        setLoading(true);

        try {
            const data = await submitAnswer(sessionId, userText);

            if (data.feedback) {
                addMessage("bot", `💡 Feedback: ${data.feedback.feedback} (Score: ${data.feedback.score}/5)`, undefined, data.feedback);
            }

            if (data.status === "completed") {
                setCompleted(true);
                addMessage("bot", data.message);
            } else {
                addMessage("bot", data.question.text, data.question.round);
            }
        } catch (error) {
            console.error("Failed to send answer:", error);
            addMessage("bot", "Error processing answer. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const addMessage = (sender: "user" | "bot", text: string, round?: string, feedback?: any) => {
        setMessages((prev) => [
            ...prev,
            { id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`, sender, text, round, feedback },
        ]);
    };

    // Get the latest bot message to display
    const activeMessage = messages.filter(m => m.sender === "bot").pop();
    const lastUserMessage = messages.filter(m => m.sender === "user").pop();

    if (!sessionId) {
        return (
            <AuroraBackground>
                <div className="fixed top-0 left-0 p-4 z-[9999] text-xs text-green-400 font-mono bg-black/90 border border-green-500/30 max-w-sm pointer-events-none hidden">
                    <div className="font-bold underline mb-1">DEBUG LOG (LOGIN_VIEW):</div>
                    {debugLogs.map((l, i) => <div key={i}>{l}</div>)}
                </div>
                <motion.div
                    initial={{ opacity: 0.0, y: 40 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3, duration: 0.8, ease: "easeInOut" }}
                    className="relative z-50 flex flex-col gap-4 items-center justify-center px-4 w-full"
                >
                    <div className="text-center space-y-4 mb-8">
                        <h1 className="text-5xl md:text-8xl font-black text-white tracking-tighter mix-blend-overlay">
                            CoPilot.AI
                        </h1>
                        <p className="text-lg md:text-xl text-neutral-400 max-w-lg mx-auto font-light">
                            Autonomous assessment protocol initiated.
                        </p>
                    </div>

                    <GlassCard className="p-8 w-full max-w-md bg-black/50 backdrop-blur-xl border border-white/10">
                        <form onSubmit={handleStart} className="flex flex-col gap-6">
                            <div className="space-y-2">
                                <label className="text-xs uppercase text-zinc-400 font-bold tracking-widest">Candidate ID</label>
                                <input
                                    type="text"
                                    placeholder="Enter your name..."
                                    value={candidateName}
                                    onChange={(e) => setCandidateName(e.target.value)}
                                    className="w-full bg-zinc-900/80 border border-zinc-700 py-4 px-4 rounded-lg text-lg text-white placeholder-zinc-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 transition-all font-medium"
                                />
                            </div>
                            <MagneticButton
                                type="submit"
                                disabled={loading || !candidateName.trim()}
                                className="w-full flex justify-center py-4 bg-white text-black hover:bg-neutral-200 font-bold"
                            >
                                {loading ? <Loader2 className="animate-spin" /> : "Initialize Session"}
                            </MagneticButton>
                        </form>
                    </GlassCard>
                </motion.div>
            </AuroraBackground>
        );
    }

    return (
        <div className="min-h-screen bg-black text-white font-sans selection:bg-purple-500/30 relative overflow-hidden flex flex-col">
            {/* Background Layer */}
            <div className="absolute inset-0 z-0 pointer-events-none">
                <AuroraBackground className="h-full">
                    <div />
                </AuroraBackground>
            </div>

            {/* Header / Status Bar */}
            <div className="relative z-50 w-full p-6 flex justify-between items-start pointer-events-none">
                <div className="pointer-events-auto">
                    <h2 className="text-xl font-bold tracking-tighter text-white/50">CoPilot.AI</h2>
                    <div className="flex items-center gap-2 mt-1">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-[10px] font-mono text-emerald-500 uppercase">Live Session</span>
                    </div>
                </div>
                {completed && (
                    <MagneticButton onClick={() => exportReport(sessionId)} className="pointer-events-auto bg-white text-black px-4 py-2 text-sm font-bold">
                        <Download size={14} className="mr-2 inline" /> Export
                    </MagneticButton>
                )}
            </div>

            {/* MAIN FOCUS AREA - CENTERED */}
            <div className="flex-1 flex flex-col items-center justify-center relative z-10 w-full max-w-4xl mx-auto px-6 mb-20">
                <AnimatePresence mode="wait">
                    {activeMessage ? (
                        <motion.div
                            key={activeMessage.id}
                            initial={{ opacity: 0, scale: 0.95, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 1.05, filter: "blur(10px)" }}
                            transition={{ duration: 0.5, ease: "easeOut" }}
                            className="w-full"
                        >
                            {/* Round Indicator */}
                            {activeMessage.round && (
                                <div className="text-center mb-6">
                                    <span className="inline-block px-3 py-1 rounded-full border border-white/10 bg-white/5 text-xs text-zinc-400 font-mono tracking-widest uppercase">
                                        // {activeMessage.round} Protocol
                                    </span>
                                </div>
                            )}

                            {/* Main Question Card */}
                            <div className="w-full">
                                {activeMessage.feedback && (
                                    <motion.div
                                        initial={{ opacity: 0, y: -10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="mb-6 p-4 rounded-xl border border-emerald-500/20 bg-emerald-900/20 backdrop-blur-md"
                                    >
                                        <div className="flex items-center gap-2 text-emerald-400 mb-1 font-mono text-xs uppercase">
                                            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full" />
                                            Feedback on previous answer
                                        </div>
                                        <p className="text-emerald-100/80 text-sm italic">"{activeMessage.text.split("\n")[0].replace("💡 Feedback: ", "")}"</p>
                                    </motion.div>
                                )}

                                <h2 className="text-3xl md:text-5xl font-bold text-white leading-tight text-center drop-shadow-2xl">
                                    {activeMessage.feedback
                                        ? activeMessage.text.split("\n").slice(1).join("\n").trim() || "Proceeding to next step..."
                                        : activeMessage.text}
                                </h2>
                            </div>
                        </motion.div>
                    ) : (
                        <div className="text-zinc-500 text-center font-mono animate-pulse">
                            [SYSTEM] Awaiting neural input...
                        </div>
                    )}
                </AnimatePresence>
            </div>

            {/* Input Area - Fixed Bottom */}
            <div className="relative z-50 w-full max-w-3xl mx-auto px-6 pb-8 md:pb-12">
                <form onSubmit={handleSend} className="relative group">
                    <div className="absolute inset-0 bg-indigo-500/20 blur-xl rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    <div className="relative flex items-center bg-zinc-900 border border-white/20 rounded-2xl p-2 shadow-2xl z-50">

                        {/* Microphone Button */}
                        <button
                            type="button"
                            onClick={toggleListening}
                            disabled={loading || completed}
                            className={`p-4 rounded-xl transition-all font-bold shrink-0 mr-2 ${isListening
                                ? "bg-red-500/20 text-red-400 animate-pulse border border-red-500/50"
                                : "text-zinc-400 hover:text-white hover:bg-white/10"}`}
                        >
                            {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                        </button>

                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            disabled={loading || completed}
                            placeholder={isListening ? "Listening..." : (completed ? "Session Terminated." : "Type your answer here...")}
                            className="flex-1 border-none p-4 text-xl focus:ring-0 focus:outline-none font-medium"
                            style={{
                                backgroundColor: '#18181b',
                                color: '#ffffff',
                                caretColor: '#ffffff',
                                opacity: 1,
                                WebkitTextFillColor: '#ffffff'
                            }}
                            autoFocus
                        />
                        <button
                            type="submit"
                            disabled={loading || completed || !input.trim()}
                            className="p-4 bg-white text-black rounded-xl hover:bg-zinc-200 transition-all font-bold disabled:opacity-50 disabled:bg-zinc-700 shrink-0"
                        >
                            {loading ? <Loader2 className="animate-spin" /> : <Send size={20} />}
                        </button>
                    </div>
                    <div className="text-center mt-3 text-xs text-zinc-600 font-mono">
                        {isListening ? "LISTENING..." : "PRESS ENTER TO SUBMIT"}
                    </div>
                </form>
            </div>
        </div>
    );
}
