import { useQuery } from '@tanstack/react-query';
import { useCallback, useEffect } from 'react';
import { useAdSettingsStore } from 'shared/store';
import { AppSelect } from 'shared/ui/appSelect';
import { getBlockPositions } from '../api';
import { BlockPosition, AppSelectOption } from 'shared/types';

const maxWidth = '100%';

export const AdPositionSelector = () => {
  const { adSettings, setBlockPosition } = useAdSettingsStore();
  const { data, isLoading } = useQuery({ queryKey: ['block-positions'], queryFn: getBlockPositions });

  useEffect(() => {
    if (!data) return;

    const defaultBlockPosition = data.find((position: BlockPosition) => position.default) || data[0];

    if (!defaultBlockPosition) return;
    setBlockPosition(defaultBlockPosition);
  }, [data]);

  const options =
    data?.map((position: BlockPosition) => ({
      value: position.id.toString(),
      label: position.block_position
    })) || [];

  const getValue = useCallback(() => {
    return adSettings.block_position
      ? options.find(
          (position: AppSelectOption) => position.value.toString() === (adSettings.block_position?.id || '').toString()
        )
      : null;
  }, [adSettings, options]);

  const onChange = useCallback(
    (newValue: unknown) => {
      const selectedPosition = data.find(
        (position: BlockPosition) => position.id.toString() === (newValue as AppSelectOption).value
      );
      if (selectedPosition) {
        setBlockPosition(selectedPosition);
      }
    },
    [data]
  );

  return (
    <AppSelect
      placeholder={isLoading ? 'Загрузка...' : 'Выберите позиционирование в блоке'}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
