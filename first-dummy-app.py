from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_docker():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Varun Sahu - DevOps Enthusiast</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

            body {
                font-family: 'Poppins', sans-serif;
                background-color: #1a1a1a;
                color: #fff;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                background-image: url('https://www.transparenttextures.com/patterns/dark-geometric.png');
                animation: moveBackground 10s linear infinite;
            }

            @keyframes moveBackground {
                from {
                    background-position: 0 0;
                }
                to {
                    background-position: 100% 100%;
                }
            }

            .container {
                text-align: center;
                background: rgba(0, 0, 0, 0.7);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                animation: fadeIn 2s ease-in-out;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                color: #00ffcc;
                animation: glow 1.5s infinite alternate;
            }

            @keyframes glow {
                from {
                    text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 30px #00ffcc;
                }
                to {
                    text-shadow: 0 0 20px #00ffcc, 0 0 30px #00ffcc, 0 0 40px #00ffcc;
                }
            }

            p {
                font-size: 1.5rem;
                margin-bottom: 2rem;
                color: #ccc;
            }

            .social-links a {
                margin: 0 15px;
                text-decoration: none;
                color: #fff;
                font-size: 1.5rem;
                transition: color 0.3s ease, transform 0.3s ease;
            }

            .social-links a:hover {
                color: #00ffcc;
                transform: scale(1.2);
            }

            .github-icon, .linkedin-icon {
                width: 32px;
                height: 32px;
                vertical-align: middle;
                transition: transform 0.3s ease;
            }

            .social-links a:hover .github-icon,
            .social-links a:hover .linkedin-icon {
                transform: rotate(360deg);
            }

            .additional-links {
                margin-top: 2rem;
            }

            .additional-links a {
                color: #00ffcc;
                text-decoration: none;
                font-size: 1.2rem;
                margin: 0 10px;
                transition: color 0.3s ease;
            }

            .additional-links a:hover {
                color: #fff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello, I'm Varun Sahu</h1>
            <p>DevOps Enthusiast | Content Creator</p>
            <div class="social-links">
                <a href="https://github.com/vaarunnsahu" target="_blank">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" class="github-icon">
                    GitHub
                </a>
                <a href="https://www.linkedin.com/in/vaarunsahu/" target="_blank">
                    <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn" class="linkedin-icon">
                    LinkedIn
                </a>
            </div>
            <div class="additional-links">
                <a href="https://twitter.com/vaarunsahu" target="_blank">Twitter</a>
                <a href="https://medium.com/@vaarunsahu" target="_blank">Medium</a>
                <a href="https://dev.to/vaarunsahu" target="_blank">Dev.to</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
