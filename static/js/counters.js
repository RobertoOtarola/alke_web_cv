/**
 * Animación de contadores numéricos para la sección de estadísticas.
 * Busca elementos con la clase '.stat-number' y anima desde 0 hasta el valor en 'data-target'.
 */
document.addEventListener('DOMContentLoaded', () => {
    const animateCounters = () => {
        const counters = document.querySelectorAll('.stat-number');
        const speed = 200; // Cuanto más alto, más lento

        counters.forEach(counter => {
            const updateCount = () => {
                const target = parseInt(counter.getAttribute('data-target'));
                const count = parseInt(counter.innerText);

                // Incremento basado en la velocidad
                const increment = Math.max(1, Math.ceil(target / speed));

                if (count < target) {
                    counter.innerText = count + increment;
                    setTimeout(updateCount, 10);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
        });
    };

    // Lazy initialization usando Intersection Observer para animar solo cuando sea visible
    const statsSection = document.getElementById('stats');
    if (statsSection) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                animateCounters();
                observer.unobserve(statsSection);
            }
        }, { threshold: 0.5 });
        observer.observe(statsSection);
    } else {
        // Fallback si no hay sección stats, intentar animar directamente
        animateCounters();
    }
});
