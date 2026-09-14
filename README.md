# LCPI Embedded Linux Kiosk & Patient Queue System

[![Platform](https://img.shields.io/badge/Platform-Allwinner%20F133%20%2F%20D1s%20%28RISC--V%29-blue.svg)](#hardware)
[![Display](https://img.shields.io/badge/Display-TFT%204.3%22%20480x272-green.svg)](#hardware)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un sistema de kiosco digital autónomo, económico y de código abierto basado en la placa con Linux Embebido **LCPI-PC-F133** y pantalla TFT de 4.3 pulgadas. Diseñado para la gestión eficiente de turnos de atención y divulgación de contenidos de promoción y prevención en salud en Instituciones Prestadoras de Servicios de Salud (IPS) y centros comunitarios.

---

## Motivación y Contexto de Aplicación

La gestión de filas y orientación al paciente en salas de espera de IPS territoriales enfrenta retos de presupuesto e infraestructura:
- **Reducción drástica de costos:** Las soluciones comerciales de "turnero" en Colombia superan los costos viables para centros de atención primaria. Este desarrollo utiliza hardware embebido de bajo consumo.
- **Optimización de recursos de Hardware:** Diseñado para ejecutarse directamente sobre el **Framebuffer de Linux (`/dev/fb0`)** en plataformas con **64 MB de RAM DDR2**, evitando la sobrecarga de servidores X11/Wayland o navegadores pesados.
- **Impacto Educativo:** Incorpora un módulo rotativo para la transmisión de mensajes de educación en salud pública durante el tiempo de espera.

---

## Arquitectura de Software

La aplicación está construida sobre Python 3 y SDL2/Pygame, optimizada para arquitectura RISC-V / ARM en Linux Embebido:
1. **Renderizado Directo:** Uso de `SDL_VIDEODRIVER=fbcon` para escritura directa en memoria de video framebuffer.
2. **Bajo Consumo de Memoria:** Footprint de memoria RAM menor a 18 MB durante ejecución continua.
3. **Frecuencia Adaptativa:** Limitación a 30 FPS para reducir el consumo térmico del procesador Allwinner F133.

---

## Estructura del Repositorio

```text
lcpi-kiosco-turnos-salud/
├── README.md
├── LICENSE
├── app/
│   ├── main.py
│   └── requirements.txt
├── docs/
│   └── setup_linux_framebuffer.md
└── hardware/
    └── lista_materiales.md
cat << 'EOF' > hardware/lista_materiales.md
# Lista de Materiales (BOM) - Kiosco Digital de Turnos

| Componente | Especificación Técnica | Función |
| :--- | :--- | :--- |
| **LCPI-PC-F133-T113-D1S-V1.3** | Chip Allwinner D1s / F133 (64MB DDR2 SiP, RISC-V) | Procesamiento central y Linux embebido |
| **FT043T48027240AC01-V01** | TFT 4.3" RGB (480x272 px) | Pantalla de visualización de interfaz |
| **Tarjeta MicroSD** | 8GB - 32GB Clase 10 | Almacenamiento de imagen de SO Linux |
| **Fuente de Alimentación** | 5V / 2A (USB Tipo-C / Conector MicroUSB) | Suministro de energía estable |
| **Gabinete / Soporte** | Impresión 3D / Acrílico corte láser | Protección ergonómica para montaje de pared IPS |
