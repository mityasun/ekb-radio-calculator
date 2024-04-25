import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FC } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

interface ProvidersProps {
  children: React.ReactNode;
}

const queryClient = new QueryClient();

export const Providers: FC<ProvidersProps> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary fallback={<p>Something went wrong</p>}>{children}</ErrorBoundary>
    </QueryClientProvider>
  );
};
