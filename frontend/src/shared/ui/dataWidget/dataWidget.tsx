import clsx from 'clsx';
import { FC, ReactElement, ReactNode } from 'react';
import s from './dataWidget.module.css';

interface DataWidgetProps {
  title: string;
  icon: ReactElement;
  children: ReactNode;
  className?: string;
  variant?: 'filled';
}

export const DataWidget: FC<DataWidgetProps> = (props) => {
  const { title, icon, children, className, variant } = props;

  return (
    <div className={clsx(s.dataWidget, className && className, variant === 'filled' && s.filled)}>
      <div className={clsx(s.dataWidgetLayout)}>
        <div className={clsx(s.dataWidgetIcon, variant === 'filled' && s.filled)}>{icon}</div>
        <div className={clsx(s.dataWidgetContent)}>
          <div className={clsx(s.dataWidgetContentData)}>{children}</div>
        </div>
      </div>
      <h5 className={clsx(s.dataWidgetTitle)}>{title}</h5>
    </div>
  );
};
