import { useCallback } from 'react';

/**
 * Scroll-reveal contract (fail-visible):
 *
 * CSS default for `.reveal` is VISIBLE. This hook adds `.is-pending`
 * (hidden, translated) synchronously during commit — before first paint —
 * so there is no flash, then swaps to `.is-visible` when the element
 * enters the viewport. If anything goes wrong (observer never fires,
 * occluded renderer, timer throttling), a bounded safety timer force-shows
 * the element — content can never remain invisible.
 *
 * Returns a callback ref; attach it directly: `ref={useReveal<HTMLDivElement>()}`.
 */
export function useReveal<T extends HTMLElement>(): (node: T | null) => void {
  return useCallback((node: T | null) => {
    if (!node || node.dataset.revealInit === '1') return;
    node.dataset.revealInit = '1';

    // Reduced motion: leave the element in its visible default state.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    // Already on screen: show without animation machinery.
    const rect = node.getBoundingClientRect();
    if (rect.top < window.innerHeight) {
      node.classList.add('is-visible');
      return;
    }

    node.classList.add('is-pending');

    const show = () => {
      node.classList.remove('is-pending');
      node.classList.add('is-visible');
    };

    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              show();
              obs.disconnect();
            }
          }
        },
        { threshold: 0.15 }
      );
      obs.observe(node);
    }

    // Safety net: never leave content hidden, whatever the renderer does.
    window.setTimeout(show, 2500);
  }, []);
}
