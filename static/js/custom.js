(function () {

	'use strict'


	AOS.init({
		duration: 800,
		easing: 'slide',
		once: true
	});


	var preloader = function() {

		var loader = document.querySelector('.loader');
		var overlay = document.getElementById('overlayer');

		function fadeOut(el) {
			if (el) {
				el.style.opacity = 1;
				(function fade() {
					if ((el.style.opacity -= .1) < 0) {
						el.style.display = "none";
					} else {
						requestAnimationFrame(fade);
					}
				})();
			}
		};

		// Wait for the DOM to be fully loaded before trying to hide preloader
		if (document.readyState === 'loading') {
			document.addEventListener('DOMContentLoaded', function() {
				setTimeout(function() {
					fadeOut(loader);
					fadeOut(overlay);
				}, 500);
			});
		} else {
			// DOM is already loaded
			setTimeout(function() {
				fadeOut(loader);
				fadeOut(overlay);
			}, 500);
		}
	};
	preloader();


	var tinyslier = function() {

		var heroSlider = document.querySelectorAll('.hero-slide');
		var propertySlider = document.querySelectorAll('.property-slider');
		var imgPropertySlider = document.querySelectorAll('.img-property-slide');
		var testimonialCenter = document.querySelectorAll('.testimonial-center');
		

		if ( heroSlider.length > 0 ) {
			var tnsHeroSlider = tns({
				container: '.hero-slide',
				mode: 'carousel',
				speed: 700,
				autoplay: true,
				controls: false,
				nav: false,
				autoplayButtonOutput: false,
				controlsContainer: '#hero-nav',
			});
		}


		if ( imgPropertySlider.length > 0 ) {
			var tnsPropertyImageSlider = tns({
				container: '.img-property-slide',
				mode: 'carousel',
				speed: 700,
				items: 1,
				autoplay: true,
				controls: false,
				nav: true,
				autoplayButtonOutput: false
			});
		}

		if ( propertySlider.length> 0 ) {
			var tnsSlider = tns({
				container: '.property-slider',
				mode: 'carousel',
				speed: 700,
				items: 3,
				autoplay: true,
				autoplayButtonOutput: false,
				controlsContainer: '#property-nav',
				responsive: {
					0: {
						items: 1
					},
					700: {
						items: 2
					},
					900: {
						items: 3
					}
				}
			});
		}



		if ( testimonialCenter.length> 0 ) {
			var testimonialSlider = tns({
				container: '#testimonial-center',
				items: 1,
				mode: 'carousel',
				slideBy: 'page',
				nav: true,
				controls: true,
				autoplay: true,
				autoplayButtonOutput: false,
				controls: true,
				gutter: 50,
				slideBy: 1,
				edgePadding: 0,
				center: true,
				controlsContainer: '#testimonial-nav',
				autoplayHoverPause: true,
				loop: true,
				swipeAngle: false,
				speed: 700,

				responsive: {
					350: {
						gutter: 10,
						edgePadding: 0,
						items: 1,
					},
					500: {
						gutter: 20,
						edgePadding: 0,
						items: 1,
					},
					700: {
						gutter: 50,
						edgePadding: 20,
						items: 2,
					},
					1000: {
						gutter: 50,
						edgePadding: 50,
						items: 2,
					}
				}

			});
		}

	}
	tinyslier();

	
	var lightboxVideo = GLightbox({
		selector: '.glightbox'
	});


	// Stats bar counter animation using data-count attribute
	var statsAnimated = false;
	var statsBar = document.querySelector('.stats-bar');

	function animateStatNumbers() {
		if (statsAnimated) return;
		statsAnimated = true;
		var statEls = document.querySelectorAll('.stat-number[data-count]');
		statEls.forEach(function(el) {
			var target = parseInt(el.getAttribute('data-count'), 10);
			var duration = 1800;
			var frameDuration = 1000 / 60;
			var totalFrames = Math.round(duration / frameDuration);
			var frame = 0;
			var counter = setInterval(function() {
				frame++;
				var progress = frame / totalFrames;
				var eased = progress * (2 - progress); // ease-out
				var current = Math.round(target * eased);
				el.textContent = current + (el.textContent.indexOf('+') !== -1 ? '+' : '');
				if (frame === totalFrames) {
					el.textContent = target + '+';
					// special case: 100% satisfaction
					if (target === 100) el.textContent = target;
					clearInterval(counter);
				}
			}, frameDuration);
		});
	}

	if (statsBar) {
		// Use IntersectionObserver if available, else run immediately
		if ('IntersectionObserver' in window) {
			var observer = new IntersectionObserver(function(entries) {
				entries.forEach(function(entry) {
					if (entry.isIntersecting) {
						animateStatNumbers();
						observer.disconnect();
					}
				});
			}, { threshold: 0.3 });
			observer.observe(statsBar);
		} else {
			animateStatNumbers();
		}
	}

})()