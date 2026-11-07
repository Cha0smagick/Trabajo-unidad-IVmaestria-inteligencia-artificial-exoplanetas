# Actividad Sumativa - Unidad 4: Inteligencia Artificial
## Clasificación Automatizada de Exoplanetas Kepler

### 📁 Entregables

| Archivo | Descripción |
|---------|-------------|
| `exoplanet_classification.ipynb` | Notebook completo **ejecutado** (con salidas): pipeline de ML de principio a fin |
| `informe_tecnico.pdf` | Informe técnico (6 páginas) |
| `informe_tecnico.tex` | Fuente LaTeX del informe |
| `figures/` | Figuras generadas por el notebook y usadas en el informe |
| `results.json` | Todas las métricas generadas por el notebook (cada cifra del informe sale de aquí) |
| `cumulative.csv` | Tabla Kepler KOI *cumulative* (NASA Exoplanet Archive, 9,564 KOIs, 50 columnas) |
| `download_dataset.py` | Descarga alternativa desde Kaggle |

---

### 🚀 Ejecución

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost lightgbm joblib
jupyter notebook exoplanet_classification.ipynb
```

El notebook usa `cumulative.csv` si está en la carpeta. Si no lo encuentra, lo descarga automáticamente de la API TAP pública del NASA Exoplanet Archive (no requiere credenciales). La semilla está fijada en 42 y la ejecución completa tarda unos 2 minutos en CPU.

Para compilar el informe: `pdflatex informe_tecnico.tex` (dos pasadas).

---

### 📊 Resultados (test hold-out, n = 1,518; IC 95 % por bootstrap con 1,000 remuestreos)

| Métrica | Valor | IC 95 % |
|---------|-------|---------|
| **ROC-AUC** | **0.979** | [0.973, 0.985] |
| **PR-AUC** (baseline 0.362) | **0.960** | [0.945, 0.972] |
| Balanced accuracy | 0.929 | [0.915, 0.942] |
| Precision (CONFIRMED) | 0.894 | [0.864, 0.920] |
| Recall (CONFIRMED) | 0.920 | [0.898, 0.942] |
| F1 (CONFIRMED) | 0.907 | [0.887, 0.924] |

**Modelo final**: LightGBM (400 árboles, `num_leaves=63`, `learning_rate=0.03`, `subsample=0.8`) sobre 16 variables físicas + 1 categórica, elegido con GridSearchCV y validación cruzada estratificada de 5 *folds*. La diferencia con XGBoost no es significativa: −0.0004 de AUC, IC 95 % [−0.002, +0.001].

**Variables dominantes**: radio planetario, SNR del tránsito, período, duración y parámetro de impacto.

---

### 🔬 Decisiones metodológicas clave

1. **Leakage explícito**: se excluyen `koi_score`, `koi_pdisposition` y `koi_fpflag_*`. Con ellas el AUC llega a 1.000 porque reproducen la decisión del catálogo.
2. **Leakage sutil**: se excluyen las columnas de incertidumbre `*_err`, porque se refinan tras la confirmación (mediana de `koi_steff_err1`: 108 K en confirmados frente a 165 K en falsos positivos). Incluirlas sube el AUC en +0.008 (IC 95 % [+0.005, +0.011]) por información del seguimiento, no por la física.
3. **Test intocado**: el algoritmo, los hiperparámetros y el umbral de decisión se eligen solo con validación cruzada sobre el entrenamiento. El umbral operativo (P ≥ 0.309) se fija con predicciones *out-of-fold*.
4. **Uso operativo**: en test, ese umbral recupera el **94.0 %** de los planetas observando solo el **39.3 %** de los KOIs, un **ahorro aproximado del 61 %** de tiempo de telescopio.
5. **Sesgos documentados**: los errores se concentran en tránsitos de baja SNR y planetas pequeños (la magnitud estelar casi no influye), además del sesgo de selección en las etiquetas y un ligero sobreajuste.

---

Dataset: NASA Exoplanet Archive, Kepler Objects of Interest (cumulative), consultado el 7 de noviembre de 2026.
