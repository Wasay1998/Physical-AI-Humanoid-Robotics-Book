import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import ChatBot from '../components/ChatBot/ChatBot';

interface LayoutWrapperProps {
  children: React.ReactNode;
  [key: string]: any; // Allow other props
}

const LayoutWrapper: React.FC<LayoutWrapperProps> = ({ children, ...props }) => {
  return (
    <Layout {...props}>
      {children}
      <BrowserOnly>
        {() => <ChatBot />}
      </BrowserOnly>
    </Layout>
  );
};

export default LayoutWrapper;