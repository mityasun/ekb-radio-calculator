import clsx from 'clsx';
import { FC, ReactElement, ReactNode } from 'react';
import s from './dataWidget.module.css';

interface DataWidgetProps {
  title: string;
  icon: ReactElement;
  children: ReactNode;
}

export const DataWidget: FC<DataWidgetProps> = (props) => {
  const { title, icon, children } = props;

  return (
    <div className={clsx(s.dataWidget)}>
      <div className={clsx(s.dataWidgetIcon)}>{icon}</div>
      <div className={clsx(s.dataWidgetContent)}>
        <div className={clsx(s.dataWidgetDataContainer)}>{children}</div>
        <h5 className={clsx(s.dataWidgetTitle)}>{title}</h5>
      </div>
    </div>
  );
};
