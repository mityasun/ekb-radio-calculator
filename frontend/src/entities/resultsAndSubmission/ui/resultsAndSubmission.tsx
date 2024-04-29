import clsx from 'clsx';
import s from './resultsAndSubmission.module.css';
import { AppButton } from 'shared/ui/appButton';
import { getResponseOrderPdf } from 'features/getOrderPdf';
import { useAdSettingsStore, useCityStore, useOrderStore } from 'shared/store';
import { useMutation } from '@tanstack/react-query';
import { OrderPdf } from 'shared/types';
import { getOrderPdf } from '../api';
import { useCalculationResults } from 'features/useCalculationResults';

export type CostAndDiscounts = Record<string, { title: string; value: string | number | null; unit?: string }>;

const BUTTON_TITLE = {
  reset: 'Сбросить медиаплан',
  savePDF: 'Сохранить медиаплан в PDF',
  sendToAproval: 'Отправить на согласование'
};

const RESULT_CONTENT = {
  blockPositionRateTitle: 'Коэффициент позиционирования в блоке:',
  seasonalRateTitle: 'Сезонный коэффициент:',
  otherPersonRateTitle: 'Коэффициент за упоминание 3-х лиц:',
  hourSelectedRateTitle: 'Коэффициент за выбор часа:',
  orderAmountWithRatesTitle: 'Сумма заказа без скидок:',
  amountDiscountTitle: 'Скидка за сумму заказа:',
  daysDiscountTitle: 'Скидка за количество дней выходов:',
  volumeDiscountTitle: 'Скидки за количество выходов в сетке:',
  totalCostTitle: 'Итого к оплате:',
  unitRub: 'руб.',
  unitPrecent: '%'
};

export const ResultsAndSubmission = () => {
  const { customer_selection, clearCustomerSelections } = useOrderStore();
  const { selectedCity } = useCityStore();
  const { adSettings, selectedRadio } = useAdSettingsStore();

  const {
    blockPositionRateValue,
    seasonalRateValue,
    otherPersonRateValue,
    hourSelectedRateeValue,
    orderAmountWithRates,
    amountDiscount,
    daysDiscount,
    volumeDiscount,
    totalCostValue
  } = useCalculationResults();

  const costAndDiscounts: CostAndDiscounts = {
    blockPositionRate: { title: RESULT_CONTENT.blockPositionRateTitle, value: blockPositionRateValue },
    seasonalRate: { title: RESULT_CONTENT.seasonalRateTitle, value: seasonalRateValue },
    otherPersonRate: { title: RESULT_CONTENT.otherPersonRateTitle, value: otherPersonRateValue },
    hourSelectedRate: { title: RESULT_CONTENT.hourSelectedRateTitle, value: hourSelectedRateeValue },
    orderAmountWithRates: {
      title: RESULT_CONTENT.orderAmountWithRatesTitle,
      value: orderAmountWithRates.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' '),
      unit: RESULT_CONTENT.unitRub
    },
    amountDiscount: {
      title: RESULT_CONTENT.amountDiscountTitle,
      value: amountDiscount,
      unit: RESULT_CONTENT.unitPrecent
    },
    daysDiscount: { title: RESULT_CONTENT.daysDiscountTitle, value: daysDiscount, unit: RESULT_CONTENT.unitPrecent },
    volumeDiscount: {
      title: RESULT_CONTENT.volumeDiscountTitle,
      value: volumeDiscount,
      unit: RESULT_CONTENT.unitPrecent
    }
  };

  const totalCost = {
    title: RESULT_CONTENT.totalCostTitle,
    value: totalCostValue.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' '),
    unit: RESULT_CONTENT.unitRub
  };

  const mutation = useMutation<void, unknown, OrderPdf>({
    mutationFn: getOrderPdf
  });

  const hanlderSavePDFClick = async () => {
    const response = getResponseOrderPdf({ selectedCity, selectedRadio, adSettings, customer_selection });
    if (!response) return;
    mutation.mutate(response);
  };

  const handlerResetCustomerSelections = () => {
    clearCustomerSelections();
  };

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
        <AppButton variant={'secondary'} onClick={handlerResetCustomerSelections}>
          {BUTTON_TITLE.reset}
        </AppButton>
        <AppButton variant={'secondary'} onClick={hanlderSavePDFClick}>
          {BUTTON_TITLE.savePDF}
        </AppButton>
        <AppButton variant={'primary'}>{BUTTON_TITLE.sendToAproval}</AppButton>
      </div>
    </div>
  );
};
