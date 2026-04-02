const { useMemo, useState } = React;

const streamlitUrl = "http://localhost:8501";

const navLinks = [
    { href: "#about", label: "About" },
    { href: "#workflow", label: "How It Works" },
    { href: "#features", label: "Features" },
    { href: "#team", label: "Team" },
];

const stats = [
    { value: "10", label: "Tomato disease classes" },
    { value: "88.31%", label: "Validation accuracy achieved" },
    { value: "Instant", label: "Prediction-ready experience" },
];

const steps = [
    {
        title: "Upload",
        body: "Choose a clear tomato leaf image in JPG, JPEG, or PNG format and send it to the detector.",
    },
    {
        title: "Analyze",
        body: "The model preprocesses the image, extracts visual patterns, and compares them against trained disease classes.",
    },
    {
        title: "Get Treatment",
        body: "Review the predicted disease, confidence score, and treatment recommendations within seconds.",
    },
];

const features = [
    {
        kicker: "Coverage",
        title: "10 diseases detected",
        body: "The model recognizes major tomato leaf conditions including bacterial, fungal, viral, pest-related, and healthy classes.",
    },
    {
        kicker: "Performance",
        title: "88% accuracy",
        body: "Built on transfer learning with MobileNetV2 to deliver strong classification performance on PlantVillage tomato data.",
    },
    {
        kicker: "Speed",
        title: "Instant results",
        body: "Designed for a practical web workflow where users upload once and get predictions without complicated setup.",
    },
    {
        kicker: "Actionability",
        title: "Treatment recommendations",
        body: "Each prediction is paired with useful next-step guidance so the app supports both detection and response.",
    },
];

const technologyPills = [
    "MobileNetV2",
    "TensorFlow",
    "Keras",
    "Streamlit",
    "PlantVillage Dataset",
    "Transfer Learning",
];

const teamMembers = [
    "Ayush Chauhan",
    "Jai Karan Gupta",
    "Kakul Mittal",
    "Vanya Kulshreshtha",
    "Yuvraj Singh",
];

function App() {
    const [menuOpen, setMenuOpen] = useState(false);

    const initials = useMemo(
        () => teamMembers.map((member) => member.split(" ").map((part) => part[0]).join("").slice(0, 2)),
        []
    );

    const closeMenu = () => setMenuOpen(false);

    return (
        <div className="site-shell">
            <header className="site-header">
                <div className="container header-inner">
                    <a className="brand" href="#top" onClick={closeMenu}>
                        <div className="brand-mark">T</div>
                        <div className="brand-copy">
                            <strong>Tomato Plant Disease Detector</strong>
                            <span>AI-powered crop health support</span>
                        </div>
                    </a>

                    <nav className={`nav ${menuOpen ? "is-open" : ""}`}>
                        {navLinks.map((link) => (
                            <a key={link.href} href={link.href} onClick={closeMenu}>
                                {link.label}
                            </a>
                        ))}
                        <a className="cta-button" href={streamlitUrl} target="_blank" rel="noreferrer" onClick={closeMenu}>
                            Try Now
                        </a>
                    </nav>

                    <button
                        className="menu-button"
                        type="button"
                        aria-label="Toggle navigation"
                        onClick={() => setMenuOpen((open) => !open)}
                    >
                        {menuOpen ? "Close" : "Menu"}
                    </button>
                </div>
            </header>

            <main id="top">
                <section className="hero">
                    <div className="container hero-grid">
                        <div>
                            <div className="eyebrow">
                                <span>Green AI</span>
                                <span>Tomato Health Screening</span>
                            </div>
                            <h1>Tomato Plant Disease Detector</h1>
                            <p>
                                A modern AI-assisted platform for identifying tomato leaf diseases, improving early
                                detection, and helping users move from diagnosis to treatment with clarity.
                            </p>

                            <div className="hero-actions">
                                <a className="cta-button" href={streamlitUrl} target="_blank" rel="noreferrer">
                                    Try Now
                                    <span>Open</span>
                                </a>
                                <a className="secondary-button" href="#about">
                                    Explore Project
                                </a>
                            </div>

                            <div className="hero-stats">
                                {stats.map((stat) => (
                                    <div className="stat-card" key={stat.label}>
                                        <strong>{stat.value}</strong>
                                        <span>{stat.label}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="hero-card">
                            <div className="mockup">
                                <div className="mockup-panel">
                                    <div className="mockup-leaf" aria-hidden="true"></div>
                                </div>
                                <div className="signal-card">
                                    <div className="signal-head">
                                        <div>
                                            <strong>AI Analysis</strong>
                                            <div className="team-meta">Live disease scoring preview</div>
                                        </div>
                                        <div className="signal-badge">Ready</div>
                                    </div>
                                    <div className="progress-group">
                                        <ProgressItem label="Target Spot" value={88} />
                                        <ProgressItem label="Early Blight" value={61} />
                                        <ProgressItem label="Leaf Mold" value={36} />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="section" id="about">
                    <div className="container">
                        <div className="section-header">
                            <div className="section-title">
                                <h2>About The Project</h2>
                                <p>
                                    This project focuses on tomato plant disease detection using computer vision and
                                    transfer learning. It combines a trained MobileNetV2 model with a Streamlit
                                    application to make disease screening approachable, fast, and practical.
                                </p>
                            </div>
                        </div>

                        <div className="about-grid">
                            <div className="panel">
                                <h3>AI Technology Used</h3>
                                <p>
                                    The detector is built on MobileNetV2 with ImageNet pretraining and a custom
                                    classification head for tomato leaf analysis. Images are resized, normalized, and
                                    evaluated to identify likely disease classes and return treatment guidance.
                                </p>
                                <div className="tech-pill-row">
                                    {technologyPills.map((pill) => (
                                        <span className="tech-pill" key={pill}>
                                            {pill}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="panel">
                                <h3>Why It Matters</h3>
                                <p>
                                    Early disease recognition helps reduce crop loss, supports better farm decisions,
                                    and allows action before symptoms spread widely. The website and app experience are
                                    designed to make that workflow quick and understandable.
                                </p>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="section" id="workflow">
                    <div className="container">
                        <div className="section-header">
                            <div className="section-title">
                                <h2>How It Works</h2>
                                <p>
                                    A simple three-step flow turns a tomato leaf image into a disease prediction with
                                    confidence scoring and guidance.
                                </p>
                            </div>
                        </div>

                        <div className="steps-grid">
                            {steps.map((step, index) => (
                                <article className="step-card" key={step.title}>
                                    <div className="step-index">{index + 1}</div>
                                    <h3>{step.title}</h3>
                                    <p>{step.body}</p>
                                </article>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="section" id="features">
                    <div className="container">
                        <div className="section-header">
                            <div className="section-title">
                                <h2>Core Features</h2>
                                <p>
                                    The project is built to be useful, explainable, and fast enough for real
                                    day-to-day crop health screening.
                                </p>
                            </div>
                        </div>

                        <div className="features-grid">
                            {features.map((feature) => (
                                <article className="feature-card" key={feature.title}>
                                    <div className="feature-topline">{feature.kicker}</div>
                                    <h3>{feature.title}</h3>
                                    <p>{feature.body}</p>
                                </article>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="section" id="team">
                    <div className="container">
                        <div className="section-header">
                            <div className="section-title">
                                <h2>Team</h2>
                                <p>
                                    Developed by a project team from GLA University, Mathura, focused on accessible,
                                    AI-driven plant disease detection.
                                </p>
                            </div>
                        </div>

                        <div className="team-grid">
                            {teamMembers.map((member, index) => (
                                <article className="team-card" key={member}>
                                    <div className="team-avatar">{initials[index]}</div>
                                    <h3>{member}</h3>
                                    <p>Tomato Plant Disease Detection Project</p>
                                    <div className="team-meta">GLA University, Mathura</div>
                                </article>
                            ))}
                        </div>
                    </div>
                </section>

                <section className="footer-cta">
                    <div className="container">
                        <div className="footer-card">
                            <div>
                                <h3>Ready to test the model?</h3>
                                <p>Launch the Streamlit app and try the tomato leaf detector in one click.</p>
                            </div>
                            <a className="cta-button" href={streamlitUrl} target="_blank" rel="noreferrer">
                                Try Now
                                <span>Open</span>
                            </a>
                        </div>
                        <div className="footer-note">
                            Tomato Plant Disease Detector Project | GLA University | 2025-26
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}

function ProgressItem({ label, value }) {
    return (
        <div className="progress-line">
            <div className="progress-meta">
                <span>{label}</span>
                <span>{value}%</span>
            </div>
            <div className="progress-track">
                <div className="progress-fill" style={{ width: `${value}%` }}></div>
            </div>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
