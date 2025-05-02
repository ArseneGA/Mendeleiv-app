document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les gestionnaires d'événements
    initEventHandlers();
    
    // Ajouter un écouteur pour le resize de la fenêtre
    window.addEventListener('resize', function() {
        // Recalculer les dimensions si nécessaire
        adjustSvgContainer();
        adjustSvgScroll();
    });

    // Fonction pour initialiser tous les gestionnaires d'événements
    function initEventHandlers() {
        // Bouton pour télécharger le SVG
        const downloadBtn = document.getElementById('downloadSvg');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', function() {
                const svgElement = document.querySelector('.svg-container svg');
                if (svgElement) {
                    downloadSVG(svgElement);
                }
            });
        }

        // Boutons pour afficher les différentes combinaisons
        const viewButtons = document.querySelectorAll('.view-combo');
        viewButtons.forEach(button => {
            // Vérifier si l'événement n'est pas déjà attaché
            if (!button.hasAttribute('data-event-attached')) {
                button.setAttribute('data-event-attached', 'true');
                button.addEventListener('click', function() {
                    try {
                        const symbolsData = this.getAttribute('data-symbols');
                        console.log('Données brutes:', symbolsData);
                        const symbols = JSON.parse(symbolsData);
                        console.log('Données parsées:', symbols);
                        
                        // Ajouter une classe pour l'animation
                        const svgContainer = document.querySelector('.svg-container');
                        if (svgContainer) {
                            svgContainer.classList.add('loading');
                            setTimeout(() => {
                                svgContainer.classList.remove('loading');
                            }, 500);
                        }
                        
                        fetchAndDisplaySVG(symbols);
                        
                        // Mettre en évidence le bouton sélectionné
                        viewButtons.forEach(btn => btn.classList.remove('active'));
                        this.classList.add('active');
                        
                        // Faire défiler jusqu'au résultat
                        document.querySelector('.result-container').scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    } catch (error) {
                        console.error('Erreur lors du parsing JSON:', error, 'Données source:', this.getAttribute('data-symbols'));
                    }
                });
            }
        });
        
        // Gérer le focus sur le champ de saisie
        const nameInput = document.getElementById('name');
        if (nameInput) {
            nameInput.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            nameInput.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        }
    }

    // Fonction pour télécharger le SVG
    function downloadSVG(svgElement) {
        // Récupérer le SVG comme une chaîne de caractères
        const svgData = new XMLSerializer().serializeToString(svgElement);
        
        // Créer un blob et un lien de téléchargement
        const blob = new Blob([svgData], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        
        // Créer un élément <a> pour déclencher le téléchargement
        const downloadLink = document.createElement('a');
        downloadLink.href = url;
        
        // Obtenir le nom du prénom à partir du texte affiché
        const nameElement = document.querySelector('h2');
        let filename = 'elements-chimiques';
        
        if (nameElement) {
            const nameMatch = nameElement.textContent.match(/"([^"]+)"/);
            if (nameMatch && nameMatch[1]) {
                filename = nameMatch[1].toLowerCase();
            }
        }
        
        downloadLink.download = `${filename}-elements-chimiques.svg`;
        
        // Ajouter, cliquer et supprimer le lien
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        
        // Libérer l'URL
        URL.revokeObjectURL(url);
        
        // Animation de confirmation
        const downloadBtn = document.getElementById('downloadSvg');
        if (downloadBtn) {
            downloadBtn.classList.add('downloaded');
            downloadBtn.textContent = 'Téléchargé ✓';
            
            setTimeout(() => {
                downloadBtn.classList.remove('downloaded');
                downloadBtn.textContent = 'Télécharger SVG';
            }, 2000);
        }
    }

    // Fonction pour récupérer et afficher un SVG basé sur une combinaison de symboles
    function fetchAndDisplaySVG(symbols) {
        fetch('/download-svg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbols: symbols })
        })
        .then(response => response.json())
        .then(data => {
            const svgContainer = document.querySelector('.svg-container');
            if (svgContainer && data.svg) {
                // Animation de transition
                svgContainer.style.opacity = 0;
                setTimeout(() => {
                    svgContainer.innerHTML = data.svg;
                    svgContainer.style.opacity = 1;
                    
                    // Ajuster la taille du conteneur
                    adjustSvgContainer();
                }, 200);
                
                // Mettre à jour le bouton de téléchargement si nécessaire
                if (!document.getElementById('downloadSvg')) {
                    const downloadContainer = document.querySelector('.download-container');
                    if (downloadContainer) {
                        const newDownloadBtn = document.createElement('button');
                        newDownloadBtn.id = 'downloadSvg';
                        newDownloadBtn.textContent = 'Télécharger SVG';
                        downloadContainer.appendChild(newDownloadBtn);
                        
                        // Réinitialiser les gestionnaires d'événements
                        initEventHandlers();
                    }
                }
                
                // Mettre à jour l'information de la combinaison actuelle
                const currentCombination = document.getElementById('current-combination');
                if (currentCombination) {
                    currentCombination.textContent = symbols.join(' + ');
                    
                    // Effet visuel pour indiquer le changement
                    currentCombination.classList.add('updated');
                    setTimeout(() => {
                        currentCombination.classList.remove('updated');
                    }, 1000);
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors de la récupération du SVG:', error);
        });
    }
    
    // Fonction pour ajuster la taille du conteneur SVG
    function adjustSvgContainer() {
        const svgElement = document.querySelector('.svg-container svg');
        const container = document.querySelector('.svg-container');
        
        if (svgElement && container) {
            const svgWidth = svgElement.getAttribute('width');
            const svgHeight = svgElement.getAttribute('height');
            
            // S'assurer que le conteneur est assez large
            if (svgWidth > container.clientWidth) {
                container.style.overflowX = 'auto';
            } else {
                container.style.overflowX = 'hidden';
            }
            
            // Ajouter un peu d'espace en bas
            container.style.minHeight = (parseInt(svgHeight) + 30) + 'px';
        }
    }
    
    // Utilisation de la délégation d'événements pour gérer les clics sur les boutons "Voir"
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('view-combo')) {
            try {
                const symbolsData = event.target.getAttribute('data-symbols');
                console.log('Délégation - Données brutes:', symbolsData);
                const symbols = JSON.parse(symbolsData);
                console.log('Délégation - Données parsées:', symbols);
                
                // Ajouter une animation de chargement
                const svgContainer = document.querySelector('.svg-container');
                if (svgContainer) {
                    svgContainer.classList.add('loading');
                    setTimeout(() => {
                        svgContainer.classList.remove('loading');
                    }, 500);
                }
                
                fetchAndDisplaySVG(symbols);
                
                // Mettre en évidence le bouton sélectionné
                document.querySelectorAll('.view-combo').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                
                // Faire défiler jusqu'au résultat
                document.querySelector('.result-container').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            } catch (error) {
                console.error('Erreur lors du parsing JSON (délégation):', error, 'Données source:', event.target.getAttribute('data-symbols'));
            }
        }
    });
    
    // Appeler adjustSvgContainer après chargement
    adjustSvgContainer();

    // Ajoute la classe d'animation à tous les éléments qui doivent être animés
    const animatedElements = [
        'header h1',
        'header .subtitle',
        '.input-group',
        '.result-container',
        '.all-combinations'
    ];
    
    animatedElements.forEach((selector, index) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {
            el.classList.add('animate-slide-up');
            el.style.animationDelay = `${0.1 + (index * 0.1)}s`;
        });
    });

    // Fonctionnalité de téléchargement SVG
    const downloadButton = document.getElementById('downloadSvg');
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            const svgElement = document.querySelector('.svg-container svg');
            if (!svgElement) return;
            
            // Récupère le contenu SVG et ajoute les attributs nécessaires
            const svgContent = svgElement.outerHTML;
            const blob = new Blob([svgContent], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);
            
            // Création d'un lien de téléchargement
            const a = document.createElement('a');
            a.href = url;
            a.download = 'mendeleiv-nom.svg';
            document.body.appendChild(a);
            a.click();
            
            // Nettoyage
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
        });
    }
    
    // Function pour ajouter des effets de survol
    function addHoverEffects() {
        const svgContainer = document.querySelector('.svg-container');
        if (!svgContainer) return;
        
        // Retirer les anciens écouteurs pour éviter les doublons
        svgContainer.removeEventListener('mousemove', handleMouseMove);
        svgContainer.removeEventListener('mouseleave', handleMouseLeave);
        
        // Ajouter les nouveaux écouteurs
        svgContainer.addEventListener('mousemove', handleMouseMove);
        svgContainer.addEventListener('mouseleave', handleMouseLeave);
    }
    
    // Fonction de gestion du mouvement de la souris
    function handleMouseMove(e) {
        const elements = document.querySelectorAll('.element-box');
        const containerRect = this.getBoundingClientRect();
        const mouseX = e.clientX - containerRect.left;
        const mouseY = e.clientY - containerRect.top;
        
        elements.forEach(el => {
            const elRect = el.getBoundingClientRect();
            const elCenterX = elRect.left - containerRect.left + elRect.width / 2;
            const elCenterY = elRect.top - containerRect.top + elRect.height / 2;
            
            // Calculer la distance
            const distance = Math.sqrt(
                Math.pow(mouseX - elCenterX, 2) + 
                Math.pow(mouseY - elCenterY, 2)
            );
            
            // Plus proche = plus grand effet
            const maxDistance = 300;
            if (distance < maxDistance) {
                const factor = 1 - (distance / maxDistance);
                const lift = 5 * factor;
                const brightness = 1 + (0.05 * factor);
                
                el.style.transform = `translateY(-${lift}px)`;
                el.style.filter = `brightness(${brightness})`;
                el.style.transition = 'transform 0.2s ease-out, filter 0.2s ease-out';
            } else {
                el.style.transform = 'translateY(0)';
                el.style.filter = 'brightness(1)';
            }
        });
    }
    
    // Fonction de gestion de la sortie de la souris
    function handleMouseLeave() {
        const elements = document.querySelectorAll('.element-box');
        elements.forEach(el => {
            el.style.transform = 'translateY(0)';
            el.style.filter = 'brightness(1)';
        });
    }
    
    // Fonction pour centrer le SVG dans le viewport si nécessaire
    function adjustSvgScroll() {
        const svgContainer = document.querySelector('.svg-container');
        const svg = svgContainer?.querySelector('svg');
        
        if (!svgContainer || !svg) return;
        
        // Récupérer les dimensions
        const svgWidth = parseFloat(svg.getAttribute('width')) || svg.getBoundingClientRect().width;
        const containerWidth = svgContainer.clientWidth;
        
        // Vérifier si le défilement est nécessaire
        if (svgWidth > containerWidth - 40) { // Tenir compte des marges
            // Mettre à jour la classe pour l'indicateur de défilement
            svgContainer.classList.add('scrollable');
            
            // Garantir que le svg est bien aligné à gauche
            svgContainer.scrollLeft = 0;
            
            // Léger délai pour s'assurer que les styles sont appliqués
            setTimeout(() => {
                // Petite animation d'indication
                requestAnimationFrame(() => {
                    svgContainer.scrollTo({
                        left: 30,
                        behavior: 'smooth'
                    });
                    
                    setTimeout(() => {
                        svgContainer.scrollTo({
                            left: 0,
                            behavior: 'smooth'
                        });
                    }, 800);
                });
            }, 500);
        } else {
            // Supprimer la classe si le défilement n'est pas nécessaire
            svgContainer.classList.remove('scrollable');
        }
        
        // Ajouter la possibilité de faire défiler avec la molette de la souris
        svgContainer.addEventListener('wheel', function(e) {
            if (svgWidth > containerWidth) {
                e.preventDefault();
                svgContainer.scrollLeft += e.deltaY;
            }
        }, { passive: false });
    }
    
    // Fonctionnalité pour voir les différentes combinaisons
    const viewButtons = document.querySelectorAll('.view-combo');
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const symbols = JSON.parse(this.getAttribute('data-symbols'));
            
            // Affichage de la combinaison sélectionnée
            const currentCombo = document.getElementById('current-combination');
            if (currentCombo) {
                currentCombo.textContent = symbols.join(' + ');
            }
            
            // Requête pour générer un nouveau SVG
            fetch('/download-svg', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ symbols })
            })
            .then(response => response.json())
            .then(data => {
                if (data.svg) {
                    const svgContainer = document.querySelector('.svg-container');
                    if (svgContainer) {
                        // Animation de transition
                        svgContainer.style.opacity = '0';
                        setTimeout(() => {
                            svgContainer.innerHTML = data.svg;
                            svgContainer.style.opacity = '1';
                            
                            // Réinitialiser les effets de survol après chargement du nouveau SVG
                            addHoverEffects();
                            
                            // Ajuster le défilement si nécessaire
                            adjustSvgScroll();
                        }, 300);
                    }
                }
            })
            .catch(error => console.error('Erreur:', error));
        });
    });
    
    // Effet de focus sur le champ de saisie
    const inputField = document.getElementById('name');
    if (inputField) {
        // Animer le focus
        inputField.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        inputField.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
        
        // Mettre le focus sur le champ au chargement de la page si vide
        if (inputField.value === '') {
            setTimeout(() => inputField.focus(), 800);
        }
    }
    
    // Initialiser les effets de survol au chargement
    addHoverEffects();
    
    // Animation subtile pour le fond au scroll
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        document.body.style.backgroundPositionY = -scrollPosition * 0.05 + 'px';
    });

    // Ajuster le défilement initial si nécessaire
    adjustSvgScroll();
}); 