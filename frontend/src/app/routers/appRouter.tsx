import { Link, Route, createRoutesFromElements, createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Layout } from '../layout';
import { MainPage } from 'pages/mainPage';
import { PrivacyPage } from 'pages/privacyPage';
import { useQuery } from '@tanstack/react-query';
import { getSystemText } from './api';
import { Helmet } from 'react-helmet-async';
import { useStore } from 'shared/store';
import { useEffect, useRef } from 'react';
import { ErrorRoutePage } from 'pages/errorRoutePage';

export const AppRouter = () => {
  const { data: systemText } = useQuery({ queryKey: ['system-text'], queryFn: getSystemText });
  const { selectedRadioId } = useStore();
  const appRef = useRef<HTMLDivElement | null>(null);
  const appStyle = window.self !== window.top ? { height: 'auto' } : { height: '100vh' };

  useEffect(() => {
    if (appRef.current) {
      const parentWindow = window.parent;
      const message = appRef.current.scrollHeight;
      parentWindow.postMessage(message, '*');
    }
  }, [appRef.current?.scrollHeight, selectedRadioId]);

  const routers = createRoutesFromElements(
    <Route path="/" element={<Layout />} handle={{ crumb: <Link to="/">Home</Link> }} errorElement={<ErrorRoutePage />}>
      <Route index element={<MainPage />} />
      <Route path="privacy" handle={{ crumb: <Link to="/privacy">Privacy</Link> }}>
        <Route index element={<PrivacyPage />} />
      </Route>
    </Route>
  );

  const router = createBrowserRouter(routers, {});

  return (
    <>
      <Helmet>
        <meta name="description" content={systemText?.seo_description && systemText.seo_description} />
        <meta name="keywords" content={systemText?.seo_keywords && systemText.seo_keywords} />
      </Helmet>
      <div style={appStyle} ref={appRef}>
        <RouterProvider router={router} />
      </div>
    </>
  );
};
