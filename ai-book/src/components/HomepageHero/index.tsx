
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Heading from '@theme/Heading';

import styles from './styles.module.css';

function HomepageHero() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="hero-background-animation"></div>
      <div className={clsx('container', styles.heroContainer)}>
        <Heading as="h1" className={styles.heroTitle}>
          Physical AI & Humanoid Robotics
        </Heading>
        <p className={styles.heroSubtitle}>
          A journey from foundational principles to building and programming intelligent humanoid robots.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/capstone-project">
            Start Reading
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="#modules">
            View Modules
          </Link>
        </div>
        <div className={styles.heroVisual}>
          {/* CSS-based robot head visual using pure CSS */}
          <div className={styles.robotHead}>
            <div className={styles.robotHeadMain}></div>
            <div className={styles.robotEyes}>
              <div className={styles.robotEye}></div>
              <div className={styles.robotEye}></div>
            </div>
            <div className={styles.robotMouth}></div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default HomepageHero;
