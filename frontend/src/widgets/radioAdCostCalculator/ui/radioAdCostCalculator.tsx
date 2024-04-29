import clsx from 'clsx';
import s from './radioAdCostCalculator.module.css';
import { AdSettingsSelector } from 'widgets/adSettingsSelector';
import { DateIntervalPicker } from 'widgets/dateIntervalPicker';
import { ResultsAndSubmission } from 'entities/resultsAndSubmission';
import { useQuery } from '@tanstack/react-query';
import { SystemText } from 'shared/types';

const DATE_INTERVAL_PICKER_TITLE = 'Выберите интервал времени';

export const RadioAdCostCalculator = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });
  const markup = { __html: systemText?.disclaimer ? systemText.disclaimer : '' };

  return (
    <div className={clsx(s.radioAdCostCalculator)}>
      <h3 className={clsx(s.radioAdCostCalculatorTitle)}>{systemText?.title && systemText.title}</h3>
      <article className={clsx(s.radioAdCostCalculatorWelcome)} dangerouslySetInnerHTML={markup} />
      <AdSettingsSelector />
      <p>
        <b>{DATE_INTERVAL_PICKER_TITLE}</b>
      </p>
      <DateIntervalPicker />
      <ResultsAndSubmission />
    </div>
  );
};
