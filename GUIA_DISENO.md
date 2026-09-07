# 🎨 GUÍA DE DISEÑO - Sistema IETS

## ✅ Cambios Implementados

### 1. **Sistema de Colores Moderno**
- **Púrpura Principal**: `#6366F1` - Color principal de la marca
- **Azul**: `#3B82F6` - Elementos secundarios
- **Verde**: `#10B981` - Estados de éxito
- **Paleta Neutral**: Grises del 50 al 900 para texto y fondos

### 2. **Componentes Rediseñados**

#### **Sidebar** (`/components/Sidebar.jsx`)
- ✅ Menú lateral permanente en desktop (280px ancho)
- ✅ Overlay deslizante en móvil
- ✅ Items con iconos y descripciones
- ✅ Secciones agrupadas (PRINCIPAL, GESTIÓN, HORARIOS, ADMINISTRACIÓN)
- ✅ Avatar y perfil de usuario en footer
- ✅ Animaciones suaves al hover
- ✅ Indicador visual del ítem activo
- ✅ Badge numérico en *Aprobar Solicitudes* para roles aprobador: suma **permisos** pendientes al nivel correspondiente y **cambios de horario** en cola (Firestore en tiempo real; ver `documentacion/flujo-roles.md`)

#### **Header** (`/components/Header.jsx`)
- ✅ Diseño minimalista con backdrop blur
- ✅ Botón de menú hamburguesa (solo móvil)
- ✅ Dropdown de usuario con perfil
- ✅ Responsive y sticky

#### **Button** (`/components/Button.jsx`)
- ✅ Componente reutilizable con 6 variantes:
  - `primary` - Púrpura principal
  - `secondary` - Gris neutral
  - `success` - Verde
  - `danger` - Rojo
  - `ghost` - Transparente
  - `outline` - Borde
- ✅ 3 tamaños: `sm`, `md`, `lg`
- ✅ Estados: normal, hover, disabled
- ✅ Soporte para iconos

#### **Dashboard** (`/app/dashboard/page.jsx`)
- ✅ Layout con Sidebar + Header + Content
- ✅ KPI Cards rediseñadas con iconos coloridos
- ✅ Gráficos modernos (Recharts)
- ✅ Tarjetas de acciones rápidas con animación
- ✅ Estados: loading, error, vacío
- ✅ Grid responsive

#### **Login** (`/app/page.jsx`)
- ✅ Pantalla fullscreen con gradiente
- ✅ Card centrada con sombras
- ✅ Botón de Google estilizado
- ✅ Animaciones sutiles
- ✅ Círculos decorativos de fondo

### 3. **Sistema Responsive**

#### **Breakpoints:**
```css
Mobile: < 768px
Tablet: 768px - 1023px
Desktop: > 1024px
```

#### **Comportamiento:**
- **Desktop** (>1024px):
  - Sidebar fijo a la izquierda
  - Content con margin-left de 280px
  - Header sin botón de menú
  
- **Tablet/Móvil** (<1024px):
  - Sidebar como overlay con backdrop
  - Content ocupa todo el ancho
  - Botón hamburguesa visible

### 4. **Tipografía**
- **Font Primary**: Inter (Google Fonts)
- **Pesos**: 300, 400, 500, 600, 700, 800
- **Tamaños**: xs (11px) → 5xl (40px)
- **Line Heights**: tight (1.25), normal (1.5), relaxed (1.75)

### 5. **Espaciado**
Sistema consistente:
```
xs: 4px   →  md: 12px  →  xl: 24px   →  3xl: 40px
sm: 8px   →  base: 16px →  2xl: 32px  →  4xl: 48px
lg: 20px  →              →             →  5xl: 64px
```

### 6. **Bordes Redondeados**
```
sm: 6px    md: 10px    lg: 12px    xl: 16px    full: 9999px
base: 8px
```

### 7. **Sombras**
5 niveles progresivos:
- `sm` - Sombra mínima para sutileza
- `base` - Sombra estándar para cards
- `md` - Sombra media para hover
- `lg` - Sombra grande para modales
- `xl` - Sombra extra grande para overlays

### 8. **Transiciones**
```
fast: 150ms  →  Para interacciones inmediatas
base: 200ms  →  Estándar para la mayoría
slow: 300ms  →  Para animaciones complejas
```

---

## 🎯 Mejores Prácticas

### **1. Usar el componente Button**
```jsx
import Button from '@/components/Button';

<Button variant="primary" size="md" onClick={handleClick}>
  Guardar
</Button>
```

### **2. Colores desde theme**
```jsx
import { colors } from '@/styles/theme';

<div style={{ color: colors.text.primary, backgroundColor: colors.backgrounds.card }}>
```

### **3. Layout con Sidebar + Header**
```jsx
<div style={{ display: 'flex', minHeight: '100vh' }}>
  <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} user={user} />
  <main className="main-content-desktop">
    <Header title="Título" onMenuClick={() => setSidebarOpen(true)} />
    <div style={{ padding: '32px' }}>
      {/* Contenido */}
    </div>
  </main>
</div>
```

### **4. KPI Cards**
```jsx
<KPICard
  title="Total"
  value={100}
  icon="📊"
  color={colors.primary.blue}
  subtitle="último mes"
/>
```

---

## 📱 Testing Responsive

### **Desktop** (>1024px)
- ✅ Sidebar visible y fija
- ✅ Content con margen izquierdo
- ✅ Sin botón hamburguesa

### **Tablet** (768px - 1023px)
- ✅ Sidebar como overlay
- ✅ Botón hamburguesa visible
- ✅ Grids ajustados a 2 columnas

### **Móvil** (<768px)
- ✅ Sidebar overlay fullscreen
- ✅ Grids en 1 columna
- ✅ Padding reducido (20px)
- ✅ Fuentes más pequeñas

---

## 🚀 Próximos Pasos

1. ✅ Theme moderno implementado
2. ✅ Sidebar y Header rediseñados
3. ✅ Dashboard actualizado
4. ✅ Login modernizado
5. ✅ Responsive completo
6. ⏳ Actualizar páginas de Permisos
7. ⏳ Actualizar páginas de Horarios
8. ⏳ Crear página de Administración

---

## 🎨 Inspiración

Diseño inspirado en:
- **Material Design 3.0**
- **Tailwind UI**
- **Vercel Design System**
- **Linear App**

---

**Última actualización**: Noviembre 2025
**Versión**: 2.0 - Diseño Moderno








