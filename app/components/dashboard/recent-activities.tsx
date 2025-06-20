
'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { 
  ShoppingCart, 
  FolderOpen, 
  User, 
  CreditCard,
  Clock
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatDateTime, getStatusColor, getStatusBadge } from '@/lib/utils';

interface Activity {
  id: string;
  type: 'order' | 'project' | 'lead' | 'payment';
  title: string;
  description: string;
  timestamp: Date;
  status?: string;
}

interface RecentActivitiesProps {
  activities: Activity[];
}

const activityIcons = {
  order: ShoppingCart,
  project: FolderOpen,
  lead: User,
  payment: CreditCard,
};

const activityColors = {
  order: 'text-blue-500',
  project: 'text-purple-500',
  lead: 'text-green-500',
  payment: 'text-orange-500',
};

export function RecentActivities({ activities }: RecentActivitiesProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
    >
      <Card className="bg-white border-0 shadow-lg">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-slate-900">
            Последние действия
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {activities.length === 0 ? (
              <div className="text-center py-8">
                <Clock className="h-12 w-12 text-slate-300 mx-auto mb-3" />
                <p className="text-slate-500">Нет недавних действий</p>
              </div>
            ) : (
              activities.map((activity, index) => {
                const Icon = activityIcons[activity.type];
                const iconColor = activityColors[activity.type];

                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.1 }}
                    className="flex items-start space-x-3 p-3 rounded-lg hover:bg-slate-50 transition-colors"
                  >
                    <div className={`p-2 rounded-lg bg-slate-100 ${iconColor}`}>
                      <Icon size={16} />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-medium text-slate-900 truncate">
                          {activity.title}
                        </h4>
                        <span className="text-xs text-slate-500 whitespace-nowrap ml-2">
                          {formatDateTime(activity.timestamp)}
                        </span>
                      </div>
                      
                      <p className="text-sm text-slate-600 mt-1">
                        {activity.description}
                      </p>
                      
                      {activity.status && (
                        <span className={`inline-block px-2 py-1 text-xs font-medium rounded-full mt-2 ${getStatusColor(activity.status)}`}>
                          {getStatusBadge(activity.status)}
                        </span>
                      )}
                    </div>
                  </motion.div>
                );
              })
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
