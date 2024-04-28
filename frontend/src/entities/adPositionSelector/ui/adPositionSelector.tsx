import { useCallback, useEffect } from 'react';
import { useAdSettingsStore } from 'shared/store';
import { AppSelect } from 'shared/ui/appSelect';
import { BlockPosition, AppSelectOption } from 'shared/types';

const maxWidth = '100%';

export const AdPositionSelector = () => {
  const { adSettings, blockPositions, setBlockPosition } = useAdSettingsStore();

  useEffect(() => {
    if (!blockPositions) return;

    const defaultBlockPosition =
      blockPositions.find((position: BlockPosition) => position.default) || blockPositions[0];

    if (!defaultBlockPosition) return;
    setBlockPosition(defaultBlockPosition);
  }, [blockPositions]);

  const options =
    blockPositions?.map((position: BlockPosition) => ({
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
      const selectedPosition = blockPositions?.find(
        (position: BlockPosition) => position.id.toString() === (newValue as AppSelectOption).value
      );
      if (selectedPosition) {
        setBlockPosition(selectedPosition);
      }
    },
    [blockPositions]
  );

  return (
    <AppSelect
      placeholder={!blockPositions ? 'Загрузка...' : 'Выберите позиционирование в блоке'}
      maxWidth={maxWidth}
      options={options}
      onChange={onChange}
      value={getValue()}
    />
  );
};
