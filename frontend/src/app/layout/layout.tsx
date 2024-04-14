import clsx from 'clsx';
import s from './layout.module.css';
import { Outlet } from 'react-router-dom';
import { Header } from '../../widgets/header';
import { Footer } from '../../widgets/footer';

export const Layout = () => {
  return (
    <div className={clsx(s.layout)}>
      <Header />
      <main className={clsx(s.layoutMain)}>
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};
