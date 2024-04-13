import clsx from 'clsx';
import s from '../styles/index.module.css';
import { Link, Route, createRoutesFromElements, createHashRouter, RouterProvider } from 'react-router-dom';
import { Layout } from '../layout';
import { MainPage } from '../../pages/mainPage';

export const AppRouter = () => {
  const routers = createRoutesFromElements(
    <Route
      path="/"
      element={<Layout />}
      handle={{ crumb: <Link to="/">Home</Link> }}
      errorElement={<p>Something went wrong</p>}>
      <Route index element={<MainPage />} />
    </Route>
  );

  const router = createHashRouter(routers, {});

  return (
    <div className={clsx(s.app)}>
      <RouterProvider router={router} />
    </div>
  );
};
