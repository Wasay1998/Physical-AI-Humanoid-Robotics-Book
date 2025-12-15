import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageHero from '@site/src/components/HomepageHero';
import ModuleCards from '@site/src/components/ModuleCards';

export default function Home(): React.ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home - ${siteConfig.title}`}
      description="A journey from foundational principles to building and programming intelligent humanoid robots.">
      <HomepageHero />
      <main>
        <div id="modules">
          <ModuleCards />
        </div>
      </main>
    </Layout>
  );
}
