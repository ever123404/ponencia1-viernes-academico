<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transporte de Contaminantes en Canal Abierto | Ponencia Internacional</title>
    <meta name="description" content="Simulación avanzada de dispersión industrial en canal artificial">
    
    <!-- React y ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            min-height: 100vh;
            color: #f8fafc;
            overflow-x: hidden;
        }
        
        .app-container {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        }
        
        .header {
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(100, 116, 139, 0.2);
            padding: 1.5rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        @media (min-width: 768px) {
            .header-content {
                flex-direction: row;
                align-items: center;
                justify-content: space-between;
            }
        }
        
        .header-title {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .header-icon {
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            padding: 0.75rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .header-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 0.25rem;
        }
        
        @media (min-width: 768px) {
            .header-text h1 {
                font-size: 1.875rem;
            }
        }
        
        .header-text p {
            font-size: 0.875rem;
            color: #cbd5e1;
        }
        
        @media (min-width: 768px) {
            .header-text p {
                font-size: 1rem;
            }
        }
        
        .main-controls {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        @media (min-width: 768px) {
            .main-controls {
                justify-content: flex-end;
            }
        }
        
        .btn {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            border-radius: 9999px;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            border: none;
            font-size: 0.875rem;
            text-decoration: none;
            white-space: nowrap;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #64748b, #475569);
            color: white;
            box-shadow: 0 4px 14px rgba(100, 116, 139, 0.3);
        }
        
        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        
        .canvas-section {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(100, 116, 139, 0.2);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }
        
        .canvas-container {
            background: #1e293b;
            border-radius: 0.75rem;
            padding: 1rem;
            border: 2px solid rgba(100, 116, 139, 0.3);
            margin-bottom: 1.5rem;
        }
        
        #simulationCanvas {
            width: 100%;
            height: auto;
            border-radius: 0.5rem;
            display: block;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .stat-card {
            background: rgba(51, 65, 85, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 0.75rem;
            padding: 1.25rem;
            text-align: center;
            border: 1px solid rgba(100, 116, 139, 0.2);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }
        
        .stat-value {
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .stat-label {
            font-size: 0.875rem;
            color: #cbd5e1;
        }
        
        .stat-blue { color: #60a5fa; }
        .stat-green { color: #34d399; }
        .stat-red { color: #f87171; }
        .stat-yellow { color: #fbbf24; }
        
        .controls-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .control-panel {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid rgba(100, 116, 139, 0.2);
        }
        
        .control-panel h3 {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #f8fafc;
        }
        
        .control-group {
            margin-bottom: 1rem;
        }
        
        .control-group label {
            display: block;
            font-size: 0.875rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-bottom: 0.5rem;
        }
        
        .slider {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #475569;
            outline: none;
            appearance: none;
            cursor: pointer;
        }
        
        .slider::-webkit-slider-thumb {
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
        }
        
        .slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            cursor: pointer;
            border: none;
            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
        }
        
        .info-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .info-panel {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid rgba(100, 116, 139, 0.2);
        }
        
        .info-panel h3 {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #f8fafc;
        }
        
        .equation {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 0.5rem;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.875rem;
            color: #e2e8f0;
            border: 1px solid rgba(100, 116, 139, 0.3);
            margin: 1rem 0;
        }
        
        .phenomena-list {
            list-style: none;
            padding: 0;
        }
        
        .phenomena-list li {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
        }
        
        .phenomena-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        
        .dot-green { background: #34d399; }
        .dot-blue { background: #60a5fa; }
        .dot-yellow { background: #fbbf24; }
        .dot-red { background: #f87171; }
        
        .footer {
            text-align: center;
            color: #94a3b8;
            padding: 2rem 1rem;
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(10px);
            border-top: 1px solid rgba(100, 116, 139, 0.2);
        }
        
        .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .footer h4 {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #f8fafc;
        }
        
        .footer p {
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .main-content {
                padding: 1rem;
            }
            
            .controls-section {
                grid-template-columns: 1fr;
            }
            
            .info-section {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .header-content {
                padding: 0 1rem;
            }
            
            .main-controls {
                width: 100%;
                justify-content: center;
            }
            
            .btn {
                flex: 1;
                justify-content: center;
                min-width: 120px;
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.6s ease-out;
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef, useCallback } = React;

        const ContaminantTransportProfessional = () => {
            const canvasRef = useRef(null);
            const animationRef = useRef(null);
            
            const [params, setParams] = useState({
                velocity: 0.5,
                diffusionX: 0.012,
                diffusionY: 0.018,
                degradation: 0.006,
                reaction: 0.002,
                spillRate: 250,
                spillPosition: 0.02,
                spillWidth: 0.2
            });
            
            const [isRunning, setIsRunning] = useState(false);
            const [time, setTime] = useState(0);
            const [maxConcentration, setMaxConcentration] = useState(0);
            const [totalMass, setTotalMass] = useState(0);
            
            const channelLength = 100;
            const channelWidth = 20;
            const gridX = 80;
            const gridY = 40;
            const dx = channelLength / gridX;
            const dy = channelWidth / gridY;
            const dt = 0.05;
            
            const concentrationRef = useRef(Array(gridY).fill().map(() => Array(gridX).fill(0)));
            const newConcentrationRef = useRef(Array(gridY).fill().map(() => Array(gridX).fill(0)));

            const updateConcentration = useCallback(() => {
                const C = concentrationRef.current;
                const newC = newConcentrationRef.current;
                const u = params.velocity;
                const Dx = params.diffusionX;
                const Dy = params.diffusionY;
                const k1 = params.degradation;
                const k2 = params.reaction;
                const spillX = Math.floor(params.spillPosition * gridX);
                const maxSpillDepth = Math.floor(params.spillWidth * gridY);
                
                let currentMax = 0;
                let mass = 0;
                
                for (let j = 0; j < gridY; j++) {
                    for (let i = 0; i < gridX; i++) {
                        let advectionX = 0;
                        let diffusionX = 0;
                        let diffusionY = 0;
                        let source = 0;
                        let reaction = -(k1 + k2) * C[j][i];
                        
                        const distanceFromNorth = j / (gridY - 1);
                        const distanceFromSouth = (gridY - 1 - j) / (gridY - 1);
                        const shoreEffect = Math.min(distanceFromNorth, distanceFromSouth);
                        const velocityProfile = 0.3 + 0.7 * (4 * shoreEffect * (1 - shoreEffect));
                        const localVelocity = u * velocityProfile;
                        
                        if (i > 0) {
                            advectionX = -localVelocity * (C[j][i] - C[j][i-1]) / dx;
                        }
                        
                        if (i > 0 && i < gridX - 1) {
                            diffusionX = Dx * (C[j][i+1] - 2*C[j][i] + C[j][i-1]) / (dx * dx);
                        }
                        
                        const mixingIntensity = 1 + 2 * shoreEffect;
                        const localDiffusionY = Dy * mixingIntensity;
                        
                        if (j > 0 && j < gridY - 1) {
                            diffusionY = localDiffusionY * (C[j+1][i] - 2*C[j][i] + C[j-1][i]) / (dy * dy);
                        }
                        
                        if (i === spillX && j <= maxSpillDepth) {
                            const distanceFromShore = j / maxSpillDepth;
                            const sourceIntensity = params.spillRate * (1 - distanceFromShore * 0.8);
                            source = sourceIntensity / (dx * dy);
                        }
                        
                        newC[j][i] = C[j][i] + dt * (advectionX + diffusionX + diffusionY + reaction + source);
                        
                        if (newC[j][i] < 0) newC[j][i] = 0;
                        
                        if (j === 0) {
                            newC[j][i] = Math.max(0, newC[j][i] * 0.95);
                        } else if (j === gridY - 1) {
                            newC[j][i] = Math.max(0, newC[j][i] * 0.85);
                        }
                        
                        currentMax = Math.max(currentMax, newC[j][i]);
                        mass += newC[j][i] * dx * dy;
                    }
                }
                
                concentrationRef.current = newC;
                newConcentrationRef.current = C;
                
                setMaxConcentration(prev => Math.max(prev, currentMax));
                setTotalMass(mass);
            }, [params]);

            const drawChannelWater = useCallback((ctx, offsetX, offsetY, simWidth, simHeight, timestamp) => {
                const waterGradient = ctx.createLinearGradient(0, offsetY, 0, offsetY + simHeight);
                waterGradient.addColorStop(0, '#4A90E2');
                waterGradient.addColorStop(0.3, '#357ABD');
                waterGradient.addColorStop(0.7, '#2E5C8A');
                waterGradient.addColorStop(1, '#1E3A5F');
                
                ctx.fillStyle = waterGradient;
                ctx.fillRect(offsetX, offsetY, simWidth, simHeight);
                
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                ctx.lineWidth = 1;
                
                for (let i = 0; i < 6; i++) {
                    ctx.beginPath();
                    const waveY = offsetY + (i + 1) * simHeight / 7;
                    const amplitude = 2;
                    const frequency = 0.015;
                    const phase = timestamp * 0.0008 + i * 0.3;
                    
                    for (let x = 0; x <= simWidth; x += 3) {
                        const y = waveY + amplitude * Math.sin(frequency * x + phase);
                        if (x === 0) {
                            ctx.moveTo(offsetX + x, y);
                        } else {
                            ctx.lineTo(offsetX + x, y);
                        }
                    }
                    ctx.stroke();
                }
            }, []);

            const drawContaminantPlume = useCallback((ctx, offsetX, offsetY, simWidth, simHeight, cellWidth, cellHeight) => {
                const C = concentrationRef.current;
                
                for (let j = 0; j < gridY; j++) {
                    for (let i = 0; i < gridX; i++) {
                        const concentration = C[j][i];
                        const normalizedConc = maxConcentration > 0 ? Math.min(concentration / maxConcentration, 1) : 0;
                        
                        if (normalizedConc > 0.01) {
                            const x = offsetX + i * cellWidth;
                            const y = offsetY + j * cellHeight;
                            
                            let red, green, blue, alpha;
                            
                            if (normalizedConc > 0.8) {
                                red = 220; green = 20; blue = 20; alpha = 0.8;
                            } else if (normalizedConc > 0.6) {
                                red = 255; green = 80; blue = 20; alpha = 0.7;
                            } else if (normalizedConc > 0.4) {
                                red = 255; green = 140; blue = 40; alpha = 0.6;
                            } else if (normalizedConc > 0.2) {
                                red = 255; green = 200; blue = 80; alpha = 0.5;
                            } else if (normalizedConc > 0.1) {
                                red = 255; green = 230; blue = 120; alpha = 0.4;
                            } else {
                                red = 255; green = 250; blue = 200; alpha = 0.3;
                            }
                            
                            const gradient = ctx.createRadialGradient(
                                x + cellWidth/2, y + cellHeight/2, 0,
                                x + cellWidth/2, y + cellHeight/2, cellWidth * 0.8
                            );
                            
                            gradient.addColorStop(0, `rgba(${red}, ${green}, ${blue}, ${alpha})`);
                            gradient.addColorStop(1, `rgba(${red}, ${green}, ${blue}, ${alpha * 0.3})`);
                            
                            ctx.fillStyle = gradient;
                            ctx.fillRect(x, y, cellWidth, cellHeight);
                        }
                    }
                }
            }, [maxConcentration]);

            const draw = useCallback(() => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                
                const ctx = canvas.getContext('2d');
                const width = canvas.width;
                const height = canvas.height;
                
                const bgGradient = ctx.createLinearGradient(0, 0, 0, height);
                bgGradient.addColorStop(0, '#0f172a');
                bgGradient.addColorStop(0.3, '#1e293b');
                bgGradient.addColorStop(1, '#334155');
                
                ctx.fillStyle = bgGradient;
                ctx.fillRect(0, 0, width, height);
                
                const isMobile = width < 768;
                const simWidth = width * (isMobile ? 0.9 : 0.85);
                const simHeight = height * 0.6;
                const offsetX = (width - simWidth) / 2;
                const offsetY = height * 0.15;
                
                drawChannelWater(ctx, offsetX, offsetY, simWidth, simHeight, Date.now());
                
                ctx.strokeStyle = 'rgba(100, 116, 139, 0.6)';
                ctx.lineWidth = 2;
                ctx.strokeRect(offsetX, offsetY, simWidth, simHeight);
                
                const cellWidth = simWidth / gridX;
                const cellHeight = simHeight / gridY;
                drawContaminantPlume(ctx, offsetX, offsetY, simWidth, simHeight, cellWidth, cellHeight);
                
                const industryX = offsetX - 50;
                const industryY = offsetY - 80;
                
                const buildingGradient = ctx.createLinearGradient(industryX, industryY, industryX, industryY + 60);
                buildingGradient.addColorStop(0, '#4a5568');
                buildingGradient.addColorStop(1, '#2d3748');
                
                ctx.fillStyle = buildingGradient;
                ctx.fillRect(industryX, industryY, 45, 60);
                ctx.fillRect(industryX + 50, industryY + 20, 30, 40);
                
                ctx.fillStyle = '#ffd700';
                for (let i = 0; i < 3; i++) {
                    for (let j = 0; j < 4; j++) {
                        ctx.fillRect(industryX + 5 + i * 12, industryY + 10 + j * 12, 6, 8);
                    }
                }
                
                ctx.fillStyle = '#2d3748';
                ctx.fillRect(industryX + 35, industryY - 25, 12, 30);
                ctx.fillRect(industryX + 55, industryY - 15, 10, 25);
                
                if (isRunning) {
                    ctx.fillStyle = 'rgba(100, 100, 100, 0.7)';
                    for (let i = 0; i < 6; i++) {
                        const smokeX = industryX + 41 + i * 4 + 2 * Math.sin(Date.now() * 0.003 + i);
                        const smokeY = industryY - 30 - i * 8;
                        ctx.beginPath();
                        ctx.arc(smokeX, smokeY, 3 + i * 0.5, 0, 2 * Math.PI);
                        ctx.fill();
                    }
                }
                
                if (isRunning || maxConcentration > 0) {
                    const dischargeX = offsetX + params.spillPosition * simWidth;
                    const dischargeY = offsetY;
                    
                    const dischargeGradient = ctx.createRadialGradient(dischargeX, dischargeY, 0, dischargeX, dischargeY, 15);
                    dischargeGradient.addColorStop(0, '#ff4444');
                    dischargeGradient.addColorStop(1, '#cc0000');
                    
                    ctx.fillStyle = dischargeGradient;
                    ctx.beginPath();
                    ctx.arc(dischargeX, dischargeY, 10, 0, 2 * Math.PI);
                    ctx.fill();
                    
                    if (isRunning) {
                        for (let i = 0; i < 4; i++) {
                            const alpha = 0.8 - i * 0.2;
                            ctx.fillStyle = `rgba(255, 100, 0, ${alpha})`;
                            ctx.beginPath();
                            ctx.arc(dischargeX + i * 3, dischargeY + i * 6, 6 - i, 0, 2 * Math.PI);
                            ctx.fill();
                        }
                    }
                }
                
                ctx.strokeStyle = '#60a5fa';
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';
                
                for (let i = 0; i < 4; i++) {
                    const arrowX = offsetX + (i + 1) * simWidth / 5;
                    const arrowY = offsetY + simHeight / 2;
                    
                    ctx.beginPath();
                    ctx.moveTo(arrowX, arrowY);
                    ctx.lineTo(arrowX + 25, arrowY);
                    ctx.lineTo(arrowX + 20, arrowY - 5);
                    ctx.moveTo(arrowX + 25, arrowY);
                    ctx.lineTo(arrowX + 20, arrowY + 5);
                    ctx.stroke();
                }
                
                ctx.fillStyle = '#f8fafc';
                ctx.font = 'bold 16px Inter, sans-serif';
                ctx.fillText('Complejo Industrial', industryX - 10, industryY - 15);
                
                ctx.font = '14px Inter, sans-serif';
                ctx.fillText('Flujo del canal →', offsetX + 50, offsetY - 40);
                
                if (isRunning || maxConcentration > 0) {
                    const dischargeX = offsetX + params.spillPosition * simWidth;
                    ctx.fillText('Descarga en orilla', dischargeX - 35, offsetY - 20);
                }
                
            }, [params, maxConcentration, isRunning, time, drawChannelWater, drawContaminantPlume]);

            useEffect(() => {
                if (isRunning) {
                    const animate = () => {
                        updateConcentration();
                        setTime(prev => prev + dt);
                        draw();
                        animationRef.current = requestAnimationFrame(animate);
                    };
                    animationRef.current = requestAnimationFrame(animate);
                } else {
                    if (animationRef.current) {
                        cancelAnimationFrame(animationRef.current);
                    }
                }
                
                return () => {
                    if (animationRef.current) {
                        cancelAnimationFrame(animationRef.current);
                    }
                };
            }, [isRunning, updateConcentration, draw]);

            useEffect(() => {
                draw();
            }, [draw, params]);

            const resetSimulation = () => {
                setIsRunning(false);
                setTime(0);
                setMaxConcentration(0);
                setTotalMass(0);
                concentrationRef.current = Array(gridY).fill().map(() => Array(gridX).fill(0));
                newConcentrationRef.current = Array(gridY).fill().map(() => Array(gridX).fill(0));
                draw();
            };

            useEffect(() => {
                const handleResize = () => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    
                    const container = canvas.parentElement;
                    const containerWidth = container.clientWidth - 32;
                    const isMobile = window.innerWidth < 768;
                    
                    canvas.width = containerWidth;
                    canvas.height = isMobile ? 400 : 500;
                    
                    draw();
                };
                
                handleResize();
                window.addEventListener('resize', handleResize);
                
                return () => window.removeEventListener('resize', handleResize);
            }, [draw]);

            return (
                <div className="app-container animate-fade-in">
                    <header className="header">
                        <div className="header-content">
                            <div className="header-title">
                                <div className="header-icon">
                                    🌊
                                </div>
                                <div className="header-text">
                                    <h1>Transporte de Contaminantes en Canal Abierto</h1>
                                    <p>Simulación avanzada de dispersión industrial en canal artificial | Ponencia Internacional</p>
                                </div>
                            </div>
                            
                            <div className="main-controls">
                                <button
                                    onClick={() => setIsRunning(!isRunning)}
                                    className={`btn ${isRunning ? 'btn-danger' : 'btn-primary'}`}
                                >
                                    {isRunning ? '⏸️ Pausar' : '▶️ Iniciar'} Simulación
                                </button>
                                
                                <button
                                    onClick={resetSimulation}
                                    className="btn btn-secondary"
                                >
                                    🔄 Reiniciar
                                </button>
                            </div>
                        </div>
                    </header>

                    <main className="main-content">
                        <section className="canvas-section">
                            <div className="canvas-container">
                                <canvas
                                    ref={canvasRef}
                                    id="simulationCanvas"
                                    width={1000}
                                    height={500}
                                />
                                
                                <div className="stats-grid">
                                    <div className="stat-card">
                                        <div className="stat-value stat-blue">{time.toFixed(1)}s</div>
                                        <div className="stat-label">Tiempo</div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-value stat-green">{totalMass.toFixed(1)} kg</div>
                                        <div className="stat-label">Masa Total</div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-value stat-red">{maxConcentration.toFixed(2)} mg/L</div>
                                        <div className="stat-label">Conc. Máxima</div>
                                    </div>
                                    <div className="stat-card">
                                        <div className="stat-value stat-yellow">{params.spillRate} kg/s</div>
                                        <div className="stat-label">Tasa Descarga</div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section className="controls-section">
                            <div className="control-panel">
                                <h3>💧 Parámetros Hidráulicos</h3>
                                
                                <div className="control-group">
                                    <label>Velocidad del canal: {params.velocity} m/s</label>
                                    <input
                                        type="range"
                                        min="0.2"
                                        max="2.0"
                                        step="0.1"
                                        value={params.velocity}
                                        onChange={(e) => setParams(prev => ({...prev, velocity: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>

                                <div className="control-group">
                                    <label>Difusión longitudinal: {params.diffusionX} m²/s</label>
                                    <input
                                        type="range"
                                        min="0.005"
                                        max="0.05"
                                        step="0.002"
                                        value={params.diffusionX}
                                        onChange={(e) => setParams(prev => ({...prev, diffusionX: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>

                                <div className="control-group">
                                    <label>Difusión transversal: {params.diffusionY} m²/s</label>
                                    <input
                                        type="range"
                                        min="0.005"
                                        max="0.05"
                                        step="0.002"
                                        value={params.diffusionY}
                                        onChange={(e) => setParams(prev => ({...prev, diffusionY: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>
                            </div>

                            <div className="control-panel">
                                <h3>🏭 Parámetros del Derrame</h3>
                                
                                <div className="control-group">
                                    <label>Intensidad de descarga: {params.spillRate} kg/s</label>
                                    <input
                                        type="range"
                                        min="50"
                                        max="500"
                                        step="25"
                                        value={params.spillRate}
                                        onChange={(e) => setParams(prev => ({...prev, spillRate: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>

                                <div className="control-group">
                                    <label>Profundidad desde orilla: {(params.spillWidth * 100).toFixed(0)}%</label>
                                    <input
                                        type="range"
                                        min="0.1"
                                        max="0.4"
                                        step="0.05"
                                        value={params.spillWidth}
                                        onChange={(e) => setParams(prev => ({...prev, spillWidth: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>
                            </div>

                            <div className="control-panel">
                                <h3>⚗️ Procesos Naturales</h3>
                                
                                <div className="control-group">
                                    <label>Degradación biológica: {params.degradation} 1/s</label>
                                    <input
                                        type="range"
                                        min="0"
                                        max="0.05"
                                        step="0.002"
                                        value={params.degradation}
                                        onChange={(e) => setParams(prev => ({...prev, degradation: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>

                                <div className="control-group">
                                    <label>Reacción química: {params.reaction} 1/s</label>
                                    <input
                                        type="range"
                                        min="0"
                                        max="0.02"
                                        step="0.001"
                                        value={params.reaction}
                                        onChange={(e) => setParams(prev => ({...prev, reaction: parseFloat(e.target.value)}))}
                                        className="slider"
                                    />
                                </div>
                            </div>
                        </section>

                        <section className="info-section">
                            <div className="info-panel">
                                <h3>📐 Modelo Matemático</h3>
                                <p><strong>Ecuación de transporte 2D:</strong></p>
                                <div className="equation">
                                    ∂C/∂t + u∂C/∂x = Dx∂²C/∂x² + Dy∂²C/∂y² - (k₁+k₂)C + S
                                </div>
                                <p style={{fontSize: '0.8rem', color: '#cbd5e1'}}>
                                    Modelo completo de advección-difusión con reacciones químicas y biológicas
                                </p>
                            </div>

                            <div className="info-panel">
                                <h3>🔬 Fenómenos Modelados</h3>
                                <ul className="phenomena-list">
                                    <li>
                                        <div className="phenomena-dot dot-green"></div>
                                        <span><strong>Advección:</strong> Transporte por flujo del canal</span>
                                    </li>
                                    <li>
                                        <div className="phenomena-dot dot-blue"></div>
                                        <span><strong>Difusión:</strong> Dispersión molecular y turbulenta</span>
                                    </li>
                                    <li>
                                        <div className="phenomena-dot dot-yellow"></div>
                                        <span><strong>Degradación:</strong> Eliminación natural progresiva</span>
                                    </li>
                                    <li>
                                        <div className="phenomena-dot dot-red"></div>
                                        <span><strong>Forma asimétrica:</strong> Pluma realista desde descarga lateral</span>
                                    </li>
                                </ul>
                            </div>
                        </section>
                    </main>

                    <footer className="footer">
                        <div className="footer-content">
                            <h4>🌊 Simulación Profesional de Transporte de Contaminantes</h4>
                            <p>Desarrollado para Ponencia Internacional | Modelo 2D de Advección-Difusión-Reacción</p>
                            <p>📚 Ideal para estudios de impacto ambiental y gestión de recursos hídricos</p>
                            <p>🎓 Herramienta educativa para ingeniería ambiental y ciencias del agua</p>
                        </div>
                    </footer>
                </div>
            );
        };

        ReactDOM.render(<ContaminantTransportProfessional />, document.getElementById('root'));
    </script>
</body>
</html>