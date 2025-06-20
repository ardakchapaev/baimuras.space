
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Package,
  AlertTriangle,
  TrendingDown,
  TrendingUp,
  Truck,
  Eye,
  Edit,
  Trash2,
  Download
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatCurrency } from '@/lib/utils';
import { Material } from '@/lib/types';

// Mock data
const mockMaterials: Material[] = [
  {
    id: '1',
    name: 'Плита МДФ 18мм',
    description: 'Влагостойкая плита МДФ для мебели',
    category: 'Плиты',
    unit: 'листы',
    unitPrice: 3500,
    stockLevel: 45,
    minStock: 10,
    supplierInfo: {
      name: 'ДревПром КГ',
      contact: '+996 312 123456'
    },
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-25')
  },
  {
    id: '2',
    name: 'Фурнитура Blum',
    description: 'Петли и направляющие Blum',
    category: 'Фурнитура',
    unit: 'комплект',
    unitPrice: 8500,
    stockLevel: 3,
    minStock: 5,
    supplierInfo: {
      name: 'Мебель-Фурнитура',
      contact: '+996 555 987654'
    },
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-30')
  },
  {
    id: '3',
    name: 'Кромка ПВХ белая',
    description: 'Кромочная лента ПВХ 2мм',
    category: 'Кромки',
    unit: 'метры',
    unitPrice: 45,
    stockLevel: 850,
    minStock: 100,
    supplierInfo: {
      name: 'Техно-Кромка',
      contact: '+996 777 456789'
    },
    createdAt: new Date('2024-01-20'),
    updatedAt: new Date('2024-02-01')
  },
  {
    id: '4',
    name: 'Лак полиуретановый',
    description: 'Защитный лак для древесины',
    category: 'Химия',
    unit: 'литры',
    unitPrice: 1200,
    stockLevel: 12,
    minStock: 5,
    supplierInfo: {
      name: 'ХимПром',
      contact: '+996 312 789012'
    },
    createdAt: new Date('2024-01-12'),
    updatedAt: new Date('2024-01-28')
  },
];

const categories = ['Все категории', 'Плиты', 'Фурнитура', 'Кромки', 'Химия', 'Крепеж'];

export default function MaterialsPage() {
  const [materials, setMaterials] = useState<Material[]>(mockMaterials);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('Все категории');

  const filteredMaterials = materials.filter(material => {
    const matchesSearch = material.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         material.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === 'Все категории' || material.category === categoryFilter;
    
    return matchesSearch && matchesCategory;
  });

  const lowStockMaterials = materials.filter(m => m.stockLevel <= m.minStock);
  const totalValue = materials.reduce((acc, m) => acc + (m.stockLevel * m.unitPrice), 0);
  const avgStockLevel = materials.reduce((acc, m) => acc + m.stockLevel, 0) / materials.length;

  const getStockStatus = (material: Material) => {
    const percentage = (material.stockLevel / material.minStock) * 100;
    if (percentage <= 100) return 'low';
    if (percentage <= 200) return 'medium';
    return 'high';
  };

  const getStockStatusColor = (status: string) => {
    switch (status) {
      case 'low': return 'text-red-600';
      case 'medium': return 'text-yellow-600';
      case 'high': return 'text-green-600';
      default: return 'text-slate-600';
    }
  };

  const getStockProgress = (material: Material) => {
    return Math.min((material.stockLevel / (material.minStock * 2)) * 100, 100);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Управление материалами</h1>
          <p className="text-slate-600">Склад и инвентаризация материалов</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Экспорт
          </Button>
          <Button variant="outline" size="sm">
            <Truck className="h-4 w-4 mr-2" />
            Поставка
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Добавить материал
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-slate-900">{materials.length}</div>
            <p className="text-sm text-slate-600">Видов материалов</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-red-600">{lowStockMaterials.length}</div>
            <p className="text-sm text-slate-600">Заканчиваются</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {formatCurrency(totalValue)}
            </div>
            <p className="text-sm text-slate-600">Стоимость склада</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {Math.round(avgStockLevel)}
            </div>
            <p className="text-sm text-slate-600">Средний остаток</p>
          </CardContent>
        </Card>
      </div>

      {/* Low Stock Alert */}
      {lowStockMaterials.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card className="bg-red-50 border-red-200">
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <AlertTriangle className="h-5 w-5 text-red-500" />
                <div>
                  <h4 className="text-sm font-medium text-red-800">
                    Требуют пополнения
                  </h4>
                  <p className="text-sm text-red-700">
                    {lowStockMaterials.length} материалов заканчиваются на складе
                  </p>
                </div>
                <Button variant="outline" size="sm" className="ml-auto">
                  Просмотреть
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <Input
                  placeholder="Поиск материалов..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Категория" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map(category => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Materials Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Материалы на складе ({filteredMaterials.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Материал</TableHead>
                  <TableHead>Категория</TableHead>
                  <TableHead>Цена за единицу</TableHead>
                  <TableHead>Остаток</TableHead>
                  <TableHead>Статус склада</TableHead>
                  <TableHead>Поставщик</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredMaterials.map((material) => {
                  const stockStatus = getStockStatus(material);
                  const stockProgress = getStockProgress(material);
                  
                  return (
                    <TableRow key={material.id}>
                      <TableCell>
                        <div className="max-w-48">
                          <div className="font-medium">{material.name}</div>
                          <div className="text-sm text-slate-500 truncate">
                            {material.description}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{material.category}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="text-right">
                          <div className="font-medium">
                            {formatCurrency(material.unitPrice)}
                          </div>
                          <div className="text-sm text-slate-500">
                            за {material.unit}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-center">
                          <div className={`font-medium ${getStockStatusColor(stockStatus)}`}>
                            {material.stockLevel} {material.unit}
                          </div>
                          <div className="text-sm text-slate-500">
                            мин. {material.minStock}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-sm">
                            {stockStatus === 'low' && (
                              <>
                                <TrendingDown className="h-4 w-4 text-red-500" />
                                <span className="text-red-600 font-medium">Мало</span>
                              </>
                            )}
                            {stockStatus === 'medium' && (
                              <>
                                <Package className="h-4 w-4 text-yellow-500" />
                                <span className="text-yellow-600 font-medium">Норма</span>
                              </>
                            )}
                            {stockStatus === 'high' && (
                              <>
                                <TrendingUp className="h-4 w-4 text-green-500" />
                                <span className="text-green-600 font-medium">Хорошо</span>
                              </>
                            )}
                          </div>
                          <Progress 
                            value={stockProgress} 
                            className={`h-2 ${
                              stockStatus === 'low' ? '[&>div]:bg-red-500' :
                              stockStatus === 'medium' ? '[&>div]:bg-yellow-500' :
                              '[&>div]:bg-green-500'
                            }`}
                          />
                        </div>
                      </TableCell>
                      <TableCell>
                        {material.supplierInfo && (
                          <div className="text-sm">
                            <div className="font-medium">
                              {(material.supplierInfo as any).name}
                            </div>
                            <div className="text-slate-500">
                              {(material.supplierInfo as any).contact}
                            </div>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Быстрые действия</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Plus className="h-6 w-6" />
                <span className="text-sm">Добавить материал</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Truck className="h-6 w-6" />
                <span className="text-sm">Новая поставка</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <AlertTriangle className="h-6 w-6" />
                <span className="text-sm">Критические остатки</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Download className="h-6 w-6" />
                <span className="text-sm">Отчет по складу</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
