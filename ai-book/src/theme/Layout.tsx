import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ChatBot from '../components/ChatBot/ChatBot';

type LayoutProps = {
  children: React.ReactNode;
  [key: string]: any;
};

const Layout: React.FC<LayoutProps> = (props) => {
  return (
    <>
      <OriginalLayout {...props}>{props.children}</OriginalLayout>
      <BrowserOnly>
        {() => <ChatBot />}
      </BrowserOnly>
    </>
  );
};

export default Layout;