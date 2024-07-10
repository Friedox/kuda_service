const loadYandexMapScript = () => {
    return new Promise((resolve, reject) => {
        if (window.ymaps) {
            resolve(window.ymaps);
            return;
        }

        const scriptElement = document.querySelector('script[src*="api-maps.yandex.ru"]');
        if (scriptElement) {
            scriptElement.onload = () => resolve(window.ymaps);
            scriptElement.onerror = () => reject(new Error('Failed to load Yandex Maps API script.'));
            return;
        }

        const script = document.createElement('script');
        script.src = `https://api-maps.yandex.ru/2.1/?apikey=2d7d974c-4c95-4115-a3e5-8a33651cb060&lang=en_US`;
        script.type = 'text/javascript';
        script.async = true;
        script.onload = () => resolve(window.ymaps);
        script.onerror = () => reject(new Error('Failed to load Yandex Maps API script.'));
        document.body.appendChild(script);
    });
};

export default loadYandexMapScript;
