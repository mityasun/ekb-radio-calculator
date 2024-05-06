import clsx from 'clsx';
import s from './layout.module.css';
import { Outlet } from 'react-router-dom';
import { Header } from '../../widgets/header';
import { Footer } from '../../widgets/footer';
import { useEffect, useRef } from 'react';

export const Layout = () => {
  const layoutRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (layoutRef.current) {
      const parentWindow = window.parent;
      const message = layoutRef.current.scrollHeight;
      parentWindow.postMessage(message, '*');
    }
  }, [layoutRef.current?.scrollHeight]);

  return (
    <div className={clsx(s.layout)} ref={layoutRef}>
      <Header />
      <main className={clsx(s.layoutMain)}>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};
