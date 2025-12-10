import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro', // updated from 'index' to 'intro'
    {
      type: 'category',
      label: 'Module 1: ROS 2',
      items: [
        'module-1/chapter-1',
        'module-1/lesson-1-1',
        'module-1/lesson-1-2',
        'module-1/lesson-1-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Gazebo+Unity',
      items: [
        'module-2/chapter-2',
        'module-2/lesson-2-1',
        'module-2/lesson-2-2',
        'module-2/lesson-2-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      items: [
        'module-3/chapter-3',
        'module-3/lesson-3-1',
        'module-3/lesson-3-2',
        'module-3/lesson-3-3',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: VLA Systems',
      items: [
        'module-4/chapter-4',
        'module-4/lesson-4-1',
        'module-4/lesson-4-2',
        'module-4/lesson-4-3',
      ],
    },
    'capstone-project',
    'history',
  ],
};

export default sidebars;
