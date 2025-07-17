// Alternância de tema claro/escuro
function setTheme(theme) {
  if (theme === 'dark') {
    document.body.classList.add('dark');
    localStorage.setItem('theme', 'dark');
    document.getElementById('theme-icon').textContent = '🌙';
  } else {
    document.body.classList.remove('dark');
    localStorage.setItem('theme', 'light');
    document.getElementById('theme-icon').textContent = '☀️';
  }
}

function toggleTheme() {
  const isDark = document.body.classList.contains('dark');
  setTheme(isDark ? 'light' : 'dark');
}

window.addEventListener('DOMContentLoaded', function() {
  const saved = localStorage.getItem('theme');
  setTheme(saved === 'dark' ? 'dark' : 'light');

  // Formatação automática de CPF/CNPJ
  const input = document.getElementById('identificador');
  if (input) {
    input.addEventListener('input', function(e) {
      let v = input.value.replace(/\D/g, '');
      if (v.length <= 11) {
        // CPF
        v = v.replace(/(\d{3})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
      } else {
        // CNPJ
        v = v.replace(/(\d{2})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d)/, '$1/$2');
        v = v.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
      }
      input.value = v;
    });
  }

  // Loading state no botão
  const form = document.getElementById('consulta-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.classList.add('loading');
        btn.innerHTML = '<span class="loader"></span>Consultando...';
      }
    });
  }
}); 