/*
 * Theme-aware chart styling — modern colors & options for frappe-charts
 * Applies primary palette from Theme Settings CSS variables
 */
(function () {
	'use strict';

	const FRAPPE_NAMED_COLORS = new Set([
		'pink',
		'blue',
		'green',
		'grey',
		'red',
		'yellow',
		'purple',
		'teal',
		'cyan',
		'orange',
		'light-blue',
	]);

	function cssVar(name, fallback) {
		const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
		return value || fallback;
	}

	function isDarkMode() {
		const body = document.body;
		const html = document.documentElement;
		return (
			body.classList.contains('dv-dark-style') ||
			body.classList.contains('dv-theme-dark') ||
			html.getAttribute('data-theme') === 'dark' ||
			html.getAttribute('data-theme-mode') === 'dark'
		);
	}

	function flattenColors(colors) {
		return (colors || [])
			.flat(2)
			.filter((color) => color !== null && color !== undefined && color !== '');
	}

	function isHexColor(value) {
		return /^#([0-9a-f]{3}|[0-9a-f]{6}|[0-9a-f]{8})$/i.test(String(value).trim());
	}

	function getThemeChartPalette() {
		return [
			cssVar('--primary', '#007BFF'),
			cssVar('--blue-500', '#2490ef'),
			cssVar('--blue-400', '#50a6f2'),
			cssVar('--blue-600', '#1579d0'),
			cssVar('--primary-hover', '#0065cd'),
			cssVar('--blue-300', '#7cbcf5'),
			cssVar('--blue-700', '#1366ae'),
			cssVar('--blue-200', '#a7d3f9'),
		].filter(Boolean);
	}

	function getHeatmapPalette() {
		return [
			isDarkMode() ? '#2a3038' : '#eef1f6',
			cssVar('--blue-100', '#d3e9fc'),
			cssVar('--blue-300', '#7cbcf5'),
			cssVar('--blue-500', '#2490ef'),
			cssVar('--primary-hover', '#0065cd'),
		];
	}

	function shouldUseThemePalette(colors, type) {
		const flat = flattenColors(colors);

		if (!flat.length) {
			return true;
		}

		if (flat.length === 1 && isHexColor(flat[0])) {
			return false;
		}

		if (flat.every((color) => FRAPPE_NAMED_COLORS.has(String(color).toLowerCase()))) {
			return true;
		}

		if (type === 'heatmap' && flat.length <= 1) {
			return true;
		}

		return false;
	}

	function enhanceChartOptions(options) {
		if (!options || typeof options !== 'object') {
			return options;
		}

		const enhanced = Object.assign({}, options);
		const type = enhanced.type || 'bar';
		const flat = flattenColors(enhanced.colors);

		if (shouldUseThemePalette(enhanced.colors, type)) {
			if (type === 'heatmap') {
				enhanced.colors = getHeatmapPalette();
			} else if (['line', 'bar', 'percentage'].includes(type)) {
				enhanced.colors = [cssVar('--primary', '#007BFF')];
			} else {
				enhanced.colors = getThemeChartPalette();
			}
		} else if (['pie', 'donut'].includes(type) && flat.length < 3) {
			enhanced.colors = getThemeChartPalette();
		}

		if (type === 'line') {
			enhanced.lineOptions = Object.assign(
				{
					regionFill: 1,
					spline: 1,
					hideDotBorder: 1,
					dotSize: 5,
				},
				enhanced.lineOptions || {}
			);
		}

		if (type === 'bar') {
			enhanced.barOptions = Object.assign(
				{
					spaceRatio: 0.55,
				},
				enhanced.barOptions || {}
			);
		}

		if (type === 'donut') {
			enhanced.strokeWidth = enhanced.strokeWidth || 38;
		}

		return enhanced;
	}

	function patchChartConstructor() {
		if (!frappe.Chart || frappe.Chart.__rst_theme_patched) {
			return;
		}

		const OriginalChart = frappe.Chart;

		function ThemedChart(parent, options) {
			return new OriginalChart(parent, enhanceChartOptions(options));
		}

		ThemedChart.prototype = OriginalChart.prototype;
		Object.setPrototypeOf(ThemedChart, OriginalChart);
		ThemedChart.__rst_theme_patched = true;
		frappe.Chart = ThemedChart;
	}

	function init() {
		if (typeof frappe === 'undefined') {
			return;
		}
		patchChartConstructor();
	}

	$(document).ready(init);
	$(document).one('app-loaded', init);
})();
