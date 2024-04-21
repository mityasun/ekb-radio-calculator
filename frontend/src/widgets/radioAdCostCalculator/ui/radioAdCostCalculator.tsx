import clsx from 'clsx';
import s from './radioAdCostCalculator.module.css';
import { TITLE_ONLINE_CALCULATOR } from 'shared/constants';
import { AdSettingsSelector } from 'widgets/adSettingsSelector';
import { DateIntervalPicker } from 'widgets/dateIntervalPicker';
import { ResultsAndSubmission } from 'entities/resultsAndSubmission';

const WELCOME_TEXT =
  // eslint-disable-next-line max-len
  'Рассчитать стоимость размещения рекламы - это легко! Для этого не нужно отправлять запросы в рекламные агентства и "дожидаться" ответа. Вам достаточно определить хронометраж  своего ролика, задать условия по времени и количеству выходов, а программа автоматически посчитает итоговый бюджет с учетом всех возможных скидок. Помимо удобства, при формировании медиаплана онлайн на сайте вы получаете дополнительную скидку 5%!';
const DISCLAIMER = {
  title: 'Внимание!',
  content:
    // eslint-disable-next-line max-len
    'Поскольку выбранные вами рекламные блоки могут быть уже заполнены, время выхода роликов может поменяться. Для получения фактического графика после расчета выберите пункт «Отправить на согласование».'
};

const DATE_INTERVAL_PICKER_TITLE = 'Выберите интервал времени';

export const RadioAdCostCalculator = () => {
  return (
    <div className={clsx(s.radioAdCostCalculator)}>
      <h3 id="radioAdCostCalculator" className={clsx(s.radioAdCostCalculatorTitle)}>
        {TITLE_ONLINE_CALCULATOR}
      </h3>
      <article className={clsx(s.radioAdCostCalculatorWelcome)}>
        <p>{WELCOME_TEXT}</p>
        <p>
          <strong>{DISCLAIMER.title}</strong>
        </p>
        <p>
          <strong>{DISCLAIMER.content}</strong>
        </p>
      </article>
      <AdSettingsSelector />
      <p>
        <strong>{DATE_INTERVAL_PICKER_TITLE}</strong>
      </p>
      <DateIntervalPicker />
      <ResultsAndSubmission />
    </div>
  );
};
