/*
 * Branding rebrand: replace visible "ERPNext" / "Frappe" text with "Riyal System"
 * and point any "Powered by" links to the Riyal System website.
 *
 * Display-only: it rewrites text nodes and a few descriptive attributes
 * (title/placeholder/aria-label/alt). It never touches links, hrefs, code
 * editors, inputs or script/style, so functionality and routing stay intact.
 */
(function () {
	'use strict';

	if (window.__rst_branding_loaded) {
		return;
	}
	window.__rst_branding_loaded = true;

	var SITE_URL = 'https://riyalsystem.com.sa/';
	var BRAND = 'Riyal System';

	// whole-word, case-insensitive
	var WORD_RE = /\b(erpnext|frappe)\b/gi;
	var HAS_WORD = /(erpnext|frappe)/i;

	// "Powered by" marketing links to redirect to the Riyal System site
	var MARKETING_RE = /\/\/(www\.)?(erpnext\.com|frappe\.io|frappeframework\.com|frappe\.cloud|frappe\.school)/i;

	var SKIP_SELECTOR =
		'script,style,noscript,textarea,input,select,option,code,pre,kbd,samp,' +
		'[contenteditable="true"],.ace_editor,.CodeMirror,.control-value-code';

	var ATTRS = ['title', 'placeholder', 'aria-label', 'alt', 'data-original-title'];

	function rebrand(value) {
		return value.replace(WORD_RE, BRAND);
	}

	function process_text_nodes(root) {
		if (!root || !root.querySelectorAll) {
			// root may be a text node added directly
			if (root && root.nodeType === 3 && HAS_WORD.test(root.nodeValue || '')) {
				var p = root.parentElement;
				if (!p || !p.closest(SKIP_SELECTOR)) {
					root.nodeValue = rebrand(root.nodeValue);
				}
			}
			return;
		}

		var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
			acceptNode: function (node) {
				if (!node.nodeValue || !HAS_WORD.test(node.nodeValue)) {
					return NodeFilter.FILTER_REJECT;
				}
				var parent = node.parentElement;
				if (parent && parent.closest(SKIP_SELECTOR)) {
					return NodeFilter.FILTER_REJECT;
				}
				return NodeFilter.FILTER_ACCEPT;
			},
		});

		var nodes = [];
		var n;
		while ((n = walker.nextNode())) {
			nodes.push(n);
		}
		nodes.forEach(function (node) {
			node.nodeValue = rebrand(node.nodeValue);
		});
	}

	function process_attributes(root) {
		if (!root || !root.querySelectorAll) {
			return;
		}
		var selector = ATTRS.map(function (a) {
			return '[' + a + ']';
		}).join(',');
		var els = root.querySelectorAll(selector);
		var list = root.matches && root.matches(selector) ? [root] : [];
		for (var i = 0; i < els.length; i++) {
			list.push(els[i]);
		}
		list.forEach(function (el) {
			if (el.closest(SKIP_SELECTOR)) {
				return;
			}
			ATTRS.forEach(function (attr) {
				var val = el.getAttribute(attr);
				if (val && HAS_WORD.test(val)) {
					el.setAttribute(attr, rebrand(val));
				}
			});
		});
	}

	function process_powered_links(root) {
		if (!root || !root.querySelectorAll) {
			return;
		}
		var anchors = root.querySelectorAll('a[href]');
		var list = root.matches && root.matches('a[href]') ? [root] : [];
		for (var i = 0; i < anchors.length; i++) {
			list.push(anchors[i]);
		}
		list.forEach(function (a) {
			var href = a.getAttribute('href') || '';
			if (!MARKETING_RE.test(href)) {
				return;
			}
			// only redirect "Powered by" style links, not help/doc links
			var context = (a.parentElement ? a.parentElement.textContent : a.textContent) || '';
			if (!/powered\s*by/i.test(context)) {
				return;
			}
			a.setAttribute('href', SITE_URL);
			a.setAttribute('target', '_blank');
			a.setAttribute('rel', 'noopener noreferrer');
		});
	}

	function process(root) {
		try {
			process_text_nodes(root);
			process_attributes(root);
			process_powered_links(root);
		} catch (e) {
			/* never let branding break the page */
		}
	}

	function full_pass() {
		if (document.body) {
			process(document.body);
		}
	}

	// --- live updates for SPA route changes / async renders ---
	var queue = [];
	var scheduled = false;

	function flush() {
		scheduled = false;
		var batch = queue;
		queue = [];
		batch.forEach(function (node) {
			process(node);
		});
	}

	function schedule(node) {
		queue.push(node);
		if (scheduled) {
			return;
		}
		scheduled = true;
		(window.requestAnimationFrame || window.setTimeout)(flush, 50);
	}

	function start_observer() {
		if (!document.body || window.__rst_branding_observer) {
			return;
		}
		var observer = new MutationObserver(function (mutations) {
			for (var i = 0; i < mutations.length; i++) {
				var added = mutations[i].addedNodes;
				for (var j = 0; j < added.length; j++) {
					var node = added[j];
					if (node.nodeType === 1 || node.nodeType === 3) {
						schedule(node);
					}
				}
			}
		});
		observer.observe(document.body, { childList: true, subtree: true });
		window.__rst_branding_observer = observer;
	}

	function init() {
		full_pass();
		start_observer();
		// a few delayed passes for late navbar/footer rendering
		setTimeout(full_pass, 800);
		setTimeout(full_pass, 2500);
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
