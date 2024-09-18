# Monitor de Sistema

![Monitoy-Proyect-Flask-HTML-Tailwind-CSS](https://github.com/user-attachments/assets/118ea2a0-dd64-49a7-b480-f1de489b9376)

## Descripción

El **Monitor de Sistema** es una aplicación web diseñada para supervisar y visualizar en tiempo real el uso de recursos del sistema, incluyendo la CPU, la memoria y el disco. La aplicación también proporciona análisis históricos y alertas basadas en umbrales configurables para ayudar a mantener el sistema en un estado óptimo.

## Características

- **Visualización en Tiempo Real**: Muestra gráficos en tiempo real del uso de CPU, memoria y disco.
- **Historial de Datos**: Proporciona gráficos históricos de los recursos del sistema.
- **Alertas Configurables**: Permite configurar umbrales para recibir alertas cuando el uso de recursos excede los límites definidos.
- **Interfaz de Usuario Intuitiva**: Ofrece una interfaz gráfica simple para monitorear y ajustar configuraciones.
- **Modularidad y Mantenibilidad**: Estructura de código organizada en módulos y patrones de diseño para facilitar el mantenimiento y la extensión.

## Tecnologías Utilizadas

- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript, Chart.js, SweetAlert2
- **Backend**: Python, Flask, SQLite, psutil

## Instalación

### Requisitos

- Python 3.x
- Node.js (opcional, para manejar dependencias frontend si es necesario)
- SQLite (para la base de datos)

### Pasos para la Instalación

1. **Clonar el Repositorio**

    ```bash
    git clone git@github.com:jjvnz/monitory.git
    cd monitory
    ```

2. **Instalar Dependencias Backend**

    Crear un entorno virtual y activarlo:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

    Instalar las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. **Instalar Dependencias Frontend**

    Si tienes dependencias específicas para el frontend, instala las necesarias (opcional):

    ```bash
    npm install
    ```

4. **Inicializar la Base de Datos**

    La base de datos SQLite se crea automáticamente cuando se ejecuta la aplicación por primera vez. Asegúrate de que `metrics.db` esté disponible en el directorio del proyecto. La estructura de la base de datos se configura automáticamente en el archivo `app/models/db.py`.

5. **Ejecutar la Aplicación**

    Iniciar el servidor Flask usando el archivo `.flaskenv` para la configuración:

    ```bash
    flask run
    ```

    La aplicación estará disponible en `http://127.0.0.1:5000`.

## Uso

1. **Visualización de Recursos**

    Accede al dashboard para ver gráficos en tiempo real del uso de CPU, memoria y disco.

2. **Configurar Alertas**

    Ve a la sección de configuración de alertas para establecer umbrales para CPU, memoria y disco. Recibirás alertas cuando el uso de recursos exceda los límites definidos.

3. **Ver Datos Históricos**

    Accede a la sección de datos históricos para ver gráficos de uso de recursos basados en datos almacenados en la base de datos.

## Estructura del Proyecto

- **app/routes.py**: Define las rutas y lógica de la aplicación.
- **app/metrics.py**: Contiene funciones para obtener y guardar métricas.
- **app/utils.py**: Funciones utilitarias, como obtener datos históricos.
- **app/models/db.py**: Maneja la base de datos y su esquema.
- **app/templates/dashboard.html**: Plantilla HTML para el dashboard.
- **app/static/js/scripts.js**: JavaScript para la interacción con el frontend.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un **Issue** o envía un **Pull Request** con tus sugerencias o mejoras.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.

## Contacto

Para preguntas o soporte, contacta a [jjvnz.dev@outlook.com](mailto:jjvnz.dev@outlook.com).
