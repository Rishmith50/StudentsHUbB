(function () {
    const isAuth = document.body && document.body.getAttribute('data-authenticated') === 'true';
    if (isAuth && !sessionStorage.getItem('studenthub_session_active')) {
        window.location.replace('/logout');
    }
})();

(function () {
    const toggle = document.querySelector('.nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (toggle && sidebar) {
        toggle.addEventListener('click', function () {
            toggle.classList.toggle('open');
            sidebar.classList.toggle('sidebar-open');
            if (overlay) overlay.classList.toggle('show');
        });

        if (overlay) {
            overlay.addEventListener('click', function () {
                toggle.classList.remove('open');
                sidebar.classList.remove('sidebar-open');
                overlay.classList.remove('show');
            });
        }

        sidebar.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                toggle.classList.remove('open');
                sidebar.classList.remove('sidebar-open');
                if (overlay) overlay.classList.remove('show');
            });
        });
    }
})();

(function () {
    const path = window.location.pathname;

    document.querySelectorAll('.sidebar-nav a').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href === '/' && path === '/') {
            link.classList.add('active');
        } else if (href !== '/' && path.startsWith(href)) {
            link.classList.add('active');
        }
    });

    document.querySelectorAll('.topbar-nav a').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href === '/' && path === '/') {
            link.classList.add('active');
            link.style.color = 'var(--lime)';
        } else if (href !== '/' && path.startsWith(href)) {
            link.classList.add('active');
            link.style.color = 'var(--lime)';
        }
    });
})();

(function () {
    const welcomeButton = document.getElementById('welcomeButton');
    if (welcomeButton) {
        welcomeButton.addEventListener('click', function () {
            window.location.href = '/students';
        });
    }
})();

function animateCountUp(element, target, duration) {
    if (!element) return;
    const start = 0;
    const startTime = performance.now();
    const isFloat = String(target).includes('.');
    const prefix = element.dataset.prefix || '';
    const suffix = element.dataset.suffix || '';

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = start + (target - start) * ease;

        if (isFloat) {
            element.textContent = prefix + current.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + suffix;
        } else {
            element.textContent = prefix + Math.round(current).toLocaleString('en-IN') + suffix;
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-countup]').forEach(function (el) {
        const target = parseFloat(el.dataset.countup);
        if (!isNaN(target)) {
            animateCountUp(el, target, 1200);
        }
    });
});

document.addEventListener('click', function (e) {
    const link = e.target.closest('a[href="/logout"]');
    if (link) {
        sessionStorage.removeItem('studenthub_session_active');
    }
});
