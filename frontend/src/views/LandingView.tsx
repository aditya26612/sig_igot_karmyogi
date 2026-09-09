import React from 'react';
import { HomeHero } from '../components/HomeHero';

/**
 * The landing view: hero image + typewriter + stats band, nothing else.
 * Shown at website start and when clicking the brand icon in the navbar.
 */
export const LandingView: React.FC = () => (
  <div style={{ paddingBottom: '32px' }}>
    <HomeHero />
  </div>
);
