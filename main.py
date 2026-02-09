if archivo:
    df = pd.read_csv(archivo)
    
    # Paso 1: Limpiar los nombres de las columnas automáticamente
    df.columns = [c.strip().upper() for c in df.columns]
    
    # Paso 2: Mostrar qué columnas encontró la App (Útil para saber qué falta)
    st.write("### Columnas detectadas en tu archivo:")
    st.write(list(df.columns))
    
    # Paso 3: Mapeo de columnas (Aquí es donde ajustas si tus nombres son diferentes)
    columnas_necesarias = ['DEPTH', 'WOB', 'RPM', 'TORQ', 'ROP', 'TGAS']
    
    # Verificamos si están todas
    faltantes = [col for col in columnas_necesarias if col not in df.columns]
    
    if not faltantes:
        try:
            # Si todo está bien, ejecutamos la lógica del archivo engine.py
            df_res = calcular_metricas(df, diametro)
            
            # --- Aquí van tus gráficos y métricas que ya tenías ---
            st.success("✅ Datos procesados con éxito")
            st.line_chart(df_res.set_index('DEPTH')['MSE'])
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
    else:
        st.error(f"❌ Error: Faltan las siguientes columnas: {faltantes}")
        st.info("💡 Consejo: Cambia el nombre de las columnas en tu Excel/CSV para que coincidan exactamente con la lista de arriba.")
