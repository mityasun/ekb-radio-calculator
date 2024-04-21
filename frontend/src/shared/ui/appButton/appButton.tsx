import clsx from 'clsx';
import s from './appButton.module.css';
import { FC, ReactNode } from 'react';

interface AppButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant: 'primary' | 'secondary';
}
export const AppButton: FC<AppButtonProps> = ({ children, variant, ...props }) => {
  return (
    <button className={clsx(s.button, variant && s[variant])} {...props}>
      {children}
    </button>
  );
};
