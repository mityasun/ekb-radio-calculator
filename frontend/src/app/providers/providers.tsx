import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FC } from 'react';
import { ErrorBoundary } from 'react-error-boundary';
import { HelmetProvider } from 'react-helmet-async';

interface ProvidersProps {
  children: React.ReactNode;
}

const queryClient = new QueryClient({ defaultOptions: { queries: { refetchOnWindowFocus: false } } });

export const Providers: FC<ProvidersProps> = ({ children }) => {
  return (
    <ErrorBoundary fallback={<p>Something went wrong</p>}>
      <QueryClientProvider client={queryClient}>
        <HelmetProvider>{children}</HelmetProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};
