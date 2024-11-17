-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Ноя 17 2024 г., 09:55
-- Версия сервера: 11.5.2-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `starstoneapp`
--

-- --------------------------------------------------------

--
-- Структура таблицы `cardstats`
--

CREATE TABLE `cardstats` (
  `id` int(11) NOT NULL,
  `Name` varchar(512) NOT NULL DEFAULT 'keke',
  `Description` varchar(512) NOT NULL DEFAULT 'is you',
  `Health` int(11) NOT NULL DEFAULT 1,
  `Shield` int(11) DEFAULT 0,
  `ManaCost` int(11) NOT NULL DEFAULT 1,
  `Attack` int(11) NOT NULL DEFAULT 1,
  `Race` enum('Terran','Zerg','Protoss') NOT NULL DEFAULT 'Zerg',
  `Type` enum('Creature','Spell') NOT NULL DEFAULT 'Creature',
  `PlayStyle` enum('Offensive','Defensive','Versatile') NOT NULL DEFAULT 'Versatile'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `cardstats`
--

INSERT INTO `cardstats` (`id`, `Name`, `Description`, `Health`, `Shield`, `ManaCost`, `Attack`, `Race`, `Type`, `PlayStyle`) VALUES
(1, 'Dark Templar', 'Cannot be attacked on the first turn. Does not take damage when attacking', 1, 2, 4, 6, 'Protoss', 'Creature', 'Offensive'),
(2, 'Hydralisk', 'Basic ranged attacker of the zerg swarm', 5, 0, 5, 6, 'Zerg', 'Creature', 'Versatile'),
(3, 'Immortal', 'This unit\'s shield cannot take more than 2 damage in one instance', 8, 6, 4, 3, 'Protoss', 'Creature', 'Defensive'),
(4, 'Wild Mutation', 'increase hp and atk of creatures by 2', 0, 0, 3, 0, 'Zerg', 'Spell', 'Offensive'),
(5, 'Mutalisk', 'Chakrams: Attack bounces and damage is reduced by 1 (attack cannot bounce into hero)\r\nRegeneration: This unit regenerates 2 health points each turn', 4, 0, 4, 4, 'Zerg', 'Creature', 'Versatile'),
(6, 'Queen', 'Can heal  itself or another unit instead of attacking (1 health point)', 4, 0, 2, 1, 'Zerg', 'Creature', 'Defensive'),
(7, 'Roach', 'Can borrow, becoming untargetable and regenerating 2 hp per turn.', 4, 0, 3, 2, 'Zerg', 'Creature', 'Versatile'),
(8, 'Sentry', 'Protective field: blocks 1 damage recieved by itself and by nearest ally units', 1, 2, 3, 1, 'Protoss', 'Creature', 'Defensive'),
(9, 'High Templar', 'Uses storm when summoned \r\nStorm: deals 2 damage per turn to all enemy units, lasts 2 turns', 1, 2, 4, 1, 'Protoss', 'Creature', 'Defensive'),
(10, 'Ultralisk', 'Deals half of its damage to nearby units on dealing damage\r\nCan perform taunt: enemy units are forced to attack this creature', 10, 0, 8, 5, 'Zerg', 'Creature', 'Versatile'),
(11, 'Void Ray', 'Damage is increased by 2 if hits the same target as the turn before', 3, 3, 3, 3, 'Protoss', 'Creature', 'Versatile'),
(12, 'Zergling', 'Spawns 2 additional zerglings on the battlefield on entering the table', 1, 0, 1, 1, 'Zerg', 'Creature', 'Versatile'),
(13, 'Zealot', 'Can attack right after entering the table\r\nDeals damage twice, but recieves damage only once', 1, 1, 1, 1, 'Protoss', 'Creature', 'Versatile'),
(14, 'Khaydarin Amulet', 'keke', 0, 0, 2, 0, 'Protoss', 'Spell', 'Versatile'),
(15, 'Transcendence', 'keke', 0, 0, 2, 0, 'Protoss', 'Spell', 'Versatile'),
(16, 'Transfuse', 'Regen 2 hp an 2 hp on the next turn', 0, 0, 2, 3, 'Zerg', 'Spell', 'Defensive'),
(17, 'Baneling', 'Explodes on dying, dealing 1 damage to all enemy units', 1, 0, 2, 1, 'Zerg', 'Creature', 'Versatile'),
(18, 'Orbital Strike', 'Deals 2 damage to enemy creatures', 0, 0, 3, 2, 'Protoss', 'Spell', 'Defensive');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cardstats`
--
ALTER TABLE `cardstats`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `id_2` (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `cardstats`
--
ALTER TABLE `cardstats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
