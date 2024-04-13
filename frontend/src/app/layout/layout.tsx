import clsx from 'clsx';
import s from './layout.module.css';
import { Outlet } from 'react-router-dom';

export const Layout = () => {
  return (
    <div className={clsx(s.layout)}>
      <header>This is header</header>
      <main className={clsx(s.main)}>
        <Outlet />
      </main>
      <footer>This is footer</footer>
    </div>
  );
};
