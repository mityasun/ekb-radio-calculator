import clsx from 'clsx';
import s from './resultsAndSubmission.module.css';
import { AppButton } from 'shared/ui/appButton';
import { useOrder } from 'shared/store/orderStore';

export type CostAndDiscounts = Record<string, { title: string; value: string; unit?: string }>;

const costAndDiscounts: CostAndDiscounts = {
  blockPositionCoefficient: { title: 'Коэффициент за позиционирование в блоке:', value: '1.0' },
  seasonalCoefficient: { title: 'Сезонный коэффициент:', value: '1.0' },
  priceListBroadcastCost: { title: 'Стоимость трансляции прайсовая:', value: '1500', unit: 'руб.' },
  volumeDiscount: { title: 'Скидка за объем:', value: '0', unit: 'руб.' },
  adDurationDiscount: { title: 'Скидка за продолжительность РК:', value: '0', unit: 'руб.' },
  totalGridOutputDiscount: { title: 'Скидки за кол-во выходов в сетке в целом:', value: '0', unit: 'руб.' }
};

const totalCost = {
  title: 'Итого к оплате:',
  value: '1500',
  unit: 'руб.'
};

const BUTTON_TITLE = {
  reset: 'Сбросить медиаплан',
  savePDF: 'Сохранить медиаплан в PDF',
  sendToAproval: 'Отправить на согласование'
};

export const ResultsAndSubmission = () => {
  const { clearCustomerSelections } = useOrder();

  return (
    <div className={clsx(s.resultsAndSubmission)}>
      <table className={clsx(s.results)}>
        <tbody>
          {Object.keys(costAndDiscounts).map((key) => (
            <tr key={key}>
              <th>{costAndDiscounts[key as keyof typeof costAndDiscounts].title}</th>
              <td>
                <strong>{costAndDiscounts[key as keyof typeof costAndDiscounts].value}</strong>
                {' ' +
                  (costAndDiscounts[key as keyof typeof costAndDiscounts].unit
                    ? costAndDiscounts[key as keyof typeof costAndDiscounts].unit
                    : '')}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <th>
              <strong>{totalCost.title}</strong>
            </th>
            <td>
              <strong>{totalCost.value + ' ' + totalCost.unit}</strong>
            </td>
          </tr>
        </tfoot>
      </table>
      <div className={clsx(s.submission)}>
        <AppButton variant={'secondary'} onClick={clearCustomerSelections}>
          {BUTTON_TITLE.reset}
        </AppButton>
        <AppButton variant={'secondary'}>{BUTTON_TITLE.savePDF}</AppButton>
        <AppButton variant={'primary'}>{BUTTON_TITLE.sendToAproval}</AppButton>
      </div>
    </div>
  );
};