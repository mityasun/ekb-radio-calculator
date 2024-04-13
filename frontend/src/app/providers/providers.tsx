import { FC } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

interface ProvidersProps {
  children: React.ReactNode;
}

export const Providers: FC<ProvidersProps> = ({ children }) => {
  return <ErrorBoundary fallback={<p>Something went wrong</p>}>{children}</ErrorBoundary>;
};
