import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Fallback } from 'pages/fallback';
import { FC } from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { HelmetProvider } from 'react-helmet-async';

interface ProvidersProps {
  children: React.ReactNode;
}

const queryClient = new QueryClient({ defaultOptions: { queries: { refetchOnWindowFocus: false } } });

export const Providers: FC<ProvidersProps> = ({ children }) => {
  return (
    <ErrorBoundary fallbackRender={({ error }) => <Fallback error={error} />}>
      <QueryClientProvider client={queryClient}>
        <HelmetProvider>{children}</HelmetProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
