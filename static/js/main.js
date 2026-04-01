/* ============================================================
   main.js — jQuery interactivity for alke_web_cv
   Dependencies: jQuery 3.7+, Bootstrap 5.3+
   ============================================================ */

$(function () {
    'use strict';

    // ==========================================================
    // 1. DARK / LIGHT MODE TOGGLE
    // ==========================================================
    const $html       = $('html');
    const $toggle     = $('#themeToggle');
    const STORAGE_KEY = 'cv-theme';

    // Restore saved preference
    const savedTheme = localStorage.getItem(STORAGE_KEY);
    if (savedTheme) {
        $html.attr('data-bs-theme', savedTheme);
    }

    function updateIcon() {
        const isDark = $html.attr('data-bs-theme') === 'dark';
        $toggle
            .find('i')
            .removeClass('bi-moon-stars-fill bi-sun-fill')
            .addClass(isDark ? 'bi-sun-fill' : 'bi-moon-stars-fill');
    }
    updateIcon();

    $toggle.on('click', function () {
        const next = $html.attr('data-bs-theme') === 'dark' ? 'light' : 'dark';
        $html.attr('data-bs-theme', next);
        localStorage.setItem(STORAGE_KEY, next);
        updateIcon();
    });

    // ==========================================================
    // 2. NAVBAR AUTO-HIDE ON SCROLL
    // ==========================================================
    let lastScrollTop = 0;
    const $navbar     = $('.navbar-custom');
    const scrollDelta = 8;

    $(window).on('scroll', function () {
        const st = $(this).scrollTop();
        if (Math.abs(st - lastScrollTop) < scrollDelta) return;

        if (st > lastScrollTop && st > 80) {
            // Scrolling down
            $navbar.addClass('navbar-hidden');
        } else {
            // Scrolling up
            $navbar.removeClass('navbar-hidden');
        }
        lastScrollTop = st;
    });

    // ==========================================================
    // 3. SCROLL REVEAL (Intersection Observer + jQuery)
    // ==========================================================
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        $(entry.target).addClass('revealed');
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
        );

        $('.reveal, .reveal-left, .stagger-children').each(function () {
            observer.observe(this);
        });
    } else {
        // Fallback: just show everything
        $('.reveal, .reveal-left, .stagger-children').addClass('revealed');
    }

    // ==========================================================
    // 4. SMOOTH SCROLL (anchor links)
    // ==========================================================
    $('a[href^="#"]').on('click', function (e) {
        const target = $($(this).attr('href'));
        if (target.length) {
            e.preventDefault();
            $('html, body').animate(
                { scrollTop: target.offset().top - 70 },
                600,
                'swing'
            );
        }
    });

    // ==========================================================
    // 5. ANIMATED COUNTERS
    // ==========================================================
    let countersAnimated = false;

    function animateCounters() {
        if (countersAnimated) return;
        countersAnimated = true;

        $('.stat-number').each(function () {
            const $el    = $(this);
            const target = parseInt($el.data('target'), 10) || 0;
            const suffix = $el.data('suffix') || '';

            $({ count: 0 }).animate(
                { count: target },
                {
                    duration: 1800,
                    easing:   'swing',
                    step: function () {
                        $el.text(Math.floor(this.count) + suffix);
                    },
                    complete: function () {
                        $el.text(target + suffix);
                    }
                }
            );
        });
    }

    // Trigger counters when stats bar is visible
    const $statsBar = $('.stats-bar');
    if ($statsBar.length && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(
            function (entries) {
                if (entries[0].isIntersecting) {
                    animateCounters();
                    counterObserver.unobserve(entries[0].target);
                }
            },
            { threshold: 0.5 }
        );
        counterObserver.observe($statsBar[0]);
    }

    // ==========================================================
    // 6. SKILL CATEGORY FILTER
    // ==========================================================
    $('.skill-filter-btn').on('click', function () {
        const category = $(this).data('filter');

        // Toggle active state
        $('.skill-filter-btn').removeClass('active');
        $(this).addClass('active');

        if (category === 'all') {
            $('.skill-badge').fadeIn(300);
        } else {
            $('.skill-badge').each(function () {
                if ($(this).data('category') === category) {
                    $(this).fadeIn(300);
                } else {
                    $(this).fadeOut(200);
                }
            });
        }
    });

    // ==========================================================
    // 7. PROJECT SEARCH / FILTER (proyectos.html)
    // ==========================================================
    const $searchInput = $('#projectSearch');
    const $noMatchMsg  = $('.no-match-msg');

    $searchInput.on('input', function () {
        const query = $(this).val().toLowerCase().trim();
        let visibleCount = 0;

        $('.project-card').each(function () {
            const name  = $(this).find('.card-title').text().toLowerCase();
            const stack = $(this).find('.stack-tags').text().toLowerCase();
            const desc  = $(this).find('.card-text').text().toLowerCase();
            const match = name.includes(query) || stack.includes(query) || desc.includes(query);

            $(this).toggle(match);
            if (match) visibleCount++;
        });

        $noMatchMsg.toggle(visibleCount === 0 && query.length > 0);
    });

    // ==========================================================
    // 8. BACK TO TOP BUTTON
    // ==========================================================
    const $backToTop = $('.back-to-top');

    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 400) {
            $backToTop.addClass('visible');
        } else {
            $backToTop.removeClass('visible');
        }
    });

    $backToTop.on('click', function () {
        $('html, body').animate({ scrollTop: 0 }, 500, 'swing');
    });

    // ==========================================================
    // 9. BOOTSTRAP TOOLTIPS INIT
    // ==========================================================
    $('[data-bs-toggle="tooltip"]').each(function () {
        new bootstrap.Tooltip(this);
    });

    // ==========================================================
    // 10. ACTIVE NAV LINK HIGHLIGHT
    // ==========================================================
    const currentPath = window.location.pathname;
    $('.navbar-custom .nav-link').each(function () {
        const href = $(this).attr('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            $(this).addClass('active');
        }
    });
});
