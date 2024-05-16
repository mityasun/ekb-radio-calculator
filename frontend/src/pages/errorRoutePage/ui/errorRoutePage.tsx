import clsx from 'clsx';
import style from './errorRoutePage.module.css';
import { useNavigate, useRouteError } from 'react-router-dom';
import { Header } from 'widgets/header';
import { Footer } from 'widgets/footer';
import { ERROR_ROUTE_PAGE_ERROR_MESSAGE, ERROR_ROUTE_PAGE_CONTENT_TEXT } from '../configs';
import { AppButton } from 'shared/ui/appButton';
interface RejectedDataType {
  statusText: string;
  status: number;
}

export const ErrorRoutePage = () => {
  const error = useRouteError() as RejectedDataType;
  const navigate = useNavigate();

  const getStatusText = (statusText: string) => {
    const status = Object.values(ERROR_ROUTE_PAGE_ERROR_MESSAGE).find((status) => status.ERROR === statusText);
    return status ? status.MESSAGE : statusText;
  };

  return (
    <div className={clsx(style.errorRoutePageWrapper)}>
      <Header />
      <div role="alert" className={clsx(style.errorRoutePage)}>
        <h1 className={clsx(style.errorRoutePageTitle)}>{ERROR_ROUTE_PAGE_CONTENT_TEXT.TITLE}</h1>
        <span className={clsx(style.errorRoutePageStatus)}>{error?.status}</span>
        <span className={clsx(style.errorRoutePageMessage)}>{getStatusText(error?.statusText)}</span>
        <AppButton style={{ maxWidth: '300px' }} variant="primary" onClick={() => navigate('/')}>
          {ERROR_ROUTE_PAGE_CONTENT_TEXT.BUTTON_TEXT}
        </AppButton>
      </div>
      <Footer />
    </div>
  );
};
