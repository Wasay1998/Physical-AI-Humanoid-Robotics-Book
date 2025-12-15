import React from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const moduleData = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description:
      'Learn how ROS 2 acts as the nervous system of humanoid robots, covering nodes, topics, services, and Python-based control.',
    link: '/module-1/chapter-1',
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description:
      'Build realistic digital twins of humanoid robots by simulating physics, environments, and sensors like LiDAR and depth cameras.',
    link: '/module-2/chapter-2',
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
    description:
      'Explore advanced robotic perception with NVIDIA Isaac, including synthetic data generation, Visual SLAM, and humanoid navigation.',
    link: '/module-3/chapter-3',
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description:
      'Integrate large language models with robotics through voice-to-action systems, cognitive planning, and a final capstone project.',
    link: '/module-4/chapter-4',
  },
];

function ModuleCard({ title, description, link }) {
  // Extract module number from title to determine icon
  const moduleNumber = title.match(/Module (\d+)/)?.[1] || '1';

  return (
    <Link to={link} className={styles.card}>
      <div>
        <div className={styles.cardIcon}>
          <div className={`${styles.moduleIcon} ${styles[`module${moduleNumber}`]}`}>
            {moduleNumber}
          </div>
        </div>
        <Heading as="h3" className={styles.cardTitle}>{title}</Heading>
        <p className={styles.cardDescription}>{description}</p>
      </div>
    </Link>
  );
}

export default function ModuleCards(): React.ReactNode {
  return (
    <section className={styles.moduleCardsSection} id="modules">
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>Explore the Modules</Heading>
        <div className={styles.grid}>
          {moduleData.map((module, idx) => (
            <ModuleCard key={idx} {...module} />
          ))}
        </div>
      </div>
    </section>
  );
}
