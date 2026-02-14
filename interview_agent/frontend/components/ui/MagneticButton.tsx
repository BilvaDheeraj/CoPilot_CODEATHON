import { useRef, useState } from "react";
import { motion, HTMLMotionProps } from "framer-motion";

interface MagneticButtonProps extends HTMLMotionProps<"button"> {
    children: React.ReactNode;
    className?: string;
}

export const MagneticButton = ({ children, className = "", ...props }: MagneticButtonProps) => {
    const ref = useRef<HTMLButtonElement>(null);
    const [position, setPosition] = useState({ x: 0, y: 0 });

    const handleMouse = (e: React.MouseEvent) => {
        const { clientX, clientY } = e;
        const { left, top, width, height } = ref.current!.getBoundingClientRect();
        const middleX = clientX - (left + width / 2);
        const middleY = clientY - (top + height / 2);
        setPosition({ x: middleX, y: middleY });
    };

    const reset = () => {
        setPosition({ x: 0, y: 0 });
    };

    return (
        <motion.button
            ref={ref}
            onMouseMove={handleMouse}
            onMouseLeave={reset}
            animate={{ x: position.x / 4, y: position.y / 4 }} // Smooth magnetic pull
            transition={{ type: "spring", stiffness: 150, damping: 15, mass: 0.1 }}
            className={`relative px-8 py-4 rounded-full bg-white text-black font-semibold text-sm uppercase tracking-wider overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
            {...props}
        >
            <span className="relative z-10 group-hover:text-white transition-colors duration-300">{children}</span>
            <div className="absolute inset-0 bg-black scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
        </motion.button>
    );
};
