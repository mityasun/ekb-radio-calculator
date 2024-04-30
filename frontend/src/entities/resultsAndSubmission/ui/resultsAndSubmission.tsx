import clsx from 'clsx';
import s from './resultsAndSubmission.module.css';
import { AppButton } from 'shared/ui/appButton';
import { getResponseOrderPdf } from 'features/getResponseOrderPDF';
import { useAdSettingsStore, useCityStore, useOrderStore } from 'shared/store';
import { useMutation } from '@tanstack/react-query';
import { OrderPdf } from 'shared/types';
import { postOrderPdf } from '../api';
import { useCalculationResults } from 'features/useCalculationResults';
import { useState } from 'react';
import { OrderModal } from 'widgets/orderModal';
import { Tooltip } from 'react-tooltip';

export type CostAndDiscounts = Record<string, { title: string; value: string | number | null; unit?: string }>;

const BUTTON_TITLE = {
  RESET_TABLE: 'Сбросить медиаплан',
  SAVE_PDF: 'Сохранить медиаплан в PDF',
  SENT_TO_APROVAL: 'Отправить на согласование'
};

const RESULT_CONTENT_TEXT = {
  BLOCK_POSITION_RATE_TITLE: 'Коэффициент позиционирования в блоке:',
  SEASONAL_RATE_TITLE: 'Сезонный коэффициент:',
  OTHER_PERSON_RATE_TITLE: 'Коэффициент за упоминание 3-х лиц:',
  HOUR_SELECTED_RATE_TITLE: 'Коэффициент за выбор часа:',
  ORDER_AMOUNT_WITH_RATES_TITLE: 'Сумма заказа без скидок:',
  AMOUNT_DISCOUNT_TITLE: 'Скидка за сумму заказа:',
  DAYS_DISCOUNT_TITLE: 'Скидка за количество дней выходов:',
  VOLUME_DISCOUNT_TITLE: 'Скидки за количество выходов в сетке:',
  TOTAL_COST_TITLE: 'Итого к оплате:',
  UNIT_RUB: 'руб.',
  UNIT_PRECENT: '%'
};

const NUMBER_DIGIT_REGEXP = /\B(?=(\d{3})+(?!\d))/g;

const toolTipStyle = { maxWidth: '300px', backgroundColor: '#05bb75', color: '#ffffff', zIndex: 9999 };

const DATA_TOOLTIP_TEXT = 'Выберите хотябы одну дату в месяце.';

export const ResultsAndSubmission = () => {
  const { customer_selection, clearCustomerSelections } = useOrderStore();
  const { selectedCity } = useCityStore();
  const { adSettings, selectedRadio } = useAdSettingsStore();
  const [isOrderModalOpen, setOrderModalOpen] = useState<boolean>(false);
  const isDisabled = customer_selection.length === 0;

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
    blockPositionRate: { title: RESULT_CONTENT_TEXT.BLOCK_POSITION_RATE_TITLE, value: blockPositionRateValue },
    seasonalRate: { title: RESULT_CONTENT_TEXT.SEASONAL_RATE_TITLE, value: seasonalRateValue },
    otherPersonRate: { title: RESULT_CONTENT_TEXT.OTHER_PERSON_RATE_TITLE, value: otherPersonRateValue },
    hourSelectedRate: { title: RESULT_CONTENT_TEXT.HOUR_SELECTED_RATE_TITLE, value: hourSelectedRateeValue },
    orderAmountWithRates: {
      title: RESULT_CONTENT_TEXT.ORDER_AMOUNT_WITH_RATES_TITLE,
      value: orderAmountWithRates.toString().replace(NUMBER_DIGIT_REGEXP, ' '),
      unit: RESULT_CONTENT_TEXT.UNIT_RUB
    },
    amountDiscount: {
      title: RESULT_CONTENT_TEXT.AMOUNT_DISCOUNT_TITLE,
      value: amountDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    },
    daysDiscount: {
      title: RESULT_CONTENT_TEXT.DAYS_DISCOUNT_TITLE,
      value: daysDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    },
    volumeDiscount: {
      title: RESULT_CONTENT_TEXT.VOLUME_DISCOUNT_TITLE,
      value: volumeDiscount,
      unit: RESULT_CONTENT_TEXT.UNIT_PRECENT
    }
  };

  const totalCost = {
    title: RESULT_CONTENT_TEXT.TOTAL_COST_TITLE,
    value: totalCostValue.toString().replace(NUMBER_DIGIT_REGEXP, ' '),
    unit: RESULT_CONTENT_TEXT.UNIT_RUB
  };

  const mutation = useMutation<void, unknown, OrderPdf>({
    mutationFn: postOrderPdf
  });

  const handleOpenOrderModal = () => {
    setOrderModalOpen(true);
  };

  const handleCloseOrderModal = () => {
    setOrderModalOpen(false);
  };

  const hanlderSavePDFClick = async () => {
    const response = getResponseOrderPdf({ selectedCity, selectedRadio, adSettings, customer_selection });
    if (!response) return;
    mutation.mutate(response);
  };

  const handlerResetCustomerSelections = () => {
    clearCustomerSelections();
  };

  return (
    <>
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
            {BUTTON_TITLE.RESET_TABLE}
          </AppButton>
          <AppButton
            variant={'secondary'}
            onClick={hanlderSavePDFClick}
            disabled={isDisabled}
            data-tooltip-id="order-button"
            data-tooltip-content={DATA_TOOLTIP_TEXT}>
            {BUTTON_TITLE.SAVE_PDF}
          </AppButton>
          {isDisabled && <Tooltip id="order-button" place="left" style={toolTipStyle} />}
          <AppButton
            variant={'primary'}
            onClick={handleOpenOrderModal}
            disabled={isDisabled}
            data-tooltip-id="order-button"
            data-tooltip-content={DATA_TOOLTIP_TEXT}>
            {BUTTON_TITLE.SENT_TO_APROVAL}
          </AppButton>
          {isDisabled && <Tooltip id="order-button" place="left" style={toolTipStyle} />}
        </div>
      </div>
      <OrderModal isOpen={isOrderModalOpen} onClose={handleCloseOrderModal} />
    </>
  );
};
