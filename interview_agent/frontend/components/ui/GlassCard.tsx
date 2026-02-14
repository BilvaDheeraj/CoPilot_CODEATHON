import React from "react";
import { cn } from "@/lib/utils";

export const GlassCard = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => {
    return (
        <div className={cn("relative overflow-hidden bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl rounded-3xl", className)}>
            {/* Noise Texture */}
            <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />

            {/* Content */}
            <div className="relative z-10">
                {children}
            </div>
        </div>
    );
};
