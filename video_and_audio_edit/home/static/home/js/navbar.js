// JavaScript to toggle the navbar links on mobile
const navbarToggle = document.querySelector('.navbar-toggle');
const navbarLinks = document.querySelector('.navbar-links');

navbarToggle.addEventListener('click', () => {
    navbarLinks.classList.toggle('active');
    navbarToggle.classList.toggle('active');
});

// Select the hero section and create a canvas element
const heroSection = document.querySelector('.hero');
const canvas = document.createElement('canvas');
canvas.classList.add('canvas-background');
heroSection.appendChild(canvas);

const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Resize canvas when the window is resized
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

// Particle configuration
const particles = [];
const particleCount = 100;

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 5 + 1; // Random size between 1 and 6
        this.speedX = Math.random() * 2 - 1; // Horizontal speed
        this.speedY = Math.random() * 2 - 1; // Vertical speed
        this.color = `rgba(255, 255, 255, ${Math.random()})`;
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Wrap particles when they move out of bounds
        if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
        if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

// Initialize particles
for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

// Animate particles
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas

    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    requestAnimationFrame(animate);
}

// Start animation
animate();






document.querySelector('.cta-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Prevent the default jump behavior
    const target = document.querySelector('#video-section');
    target.scrollIntoView({
        behavior: 'smooth', // Smooth scrolling
        block: 'start'     // Scroll to the start of the section
    });
});


